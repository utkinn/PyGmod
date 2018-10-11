from unittest import TestCase
from unittest.mock import patch, Mock, call
import pickle

from .table_mock import TableMock
import luastack


def create_g_mock():
    return TableMock({
        'net': TableMock({
            'Start': Mock(name='net.Start'),
            'WriteUInt': Mock(name='net.WriteUInt'),
            'WriteData': Mock(name='net.WriteData'),
            'Send': Mock(name='net.Send'),
            'SendToServer': Mock(name='net.SendToServer'),
            'WriteType': Mock(name='net.WriteType'),
        }),
        'Player': Mock(name='Player'),
        'CLIENT': True
    })


@patch('gmod.lua.G', new_callable=create_g_mock)
class SendTestCase(TestCase):
    def test_wrong_message_type_name(self, g):
        from gmod import realms

        realms.CLIENT = False
        realms.SERVER = True

        from gmod.net import send
        from gmod import player

        with self.assertRaises(TypeError):
            send(123, 1)

    def test_no_receiver(self, g):
        from gmod import realms

        realms.CLIENT = False
        realms.SERVER = True

        from gmod.net import send

        with self.assertRaises(ValueError):
            send('spam', 1, 2)

    def test_from_client(self, g):
        from gmod import realms

        realms.CLIENT = True
        realms.SERVER = False

        from gmod.net import send

        data = (1, 2, 3)
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

        send('spam', *data)

        g.net.Start.assert_called_once_with('spam')
        g.net.WriteUInt.assert_called_once_with(len(pickled), 32)
        g.net.WriteData.assert_called_once_with(pickled, len(pickled))
        g.net.SendToServer.assert_called_once()

    def test_from_server(self, g):
        from gmod import realms

        realms.CLIENT = False
        realms.SERVER = True

        from gmod.net import send
        from gmod import player

        data = (2, 3, 4)
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        ply = player.get_by_userid(1)

        send('eggs', *data, receiver=ply)

        g.net.Start.assert_called_once_with('eggs')
        g.net.WriteUInt.assert_called_once_with(len(pickled), 32)
        g.net.WriteData.assert_called_once_with(pickled, len(pickled))
        g.net.Send.assert_called_once_with(ply)

    def test_no_data(self, g):
        from gmod import realms

        realms.CLIENT = True
        realms.SERVER = False

        from gmod.net import send

        pickled = pickle.dumps((), pickle.HIGHEST_PROTOCOL)

        send('foo')

        g.net.Start.assert_called_once_with('foo')
        g.net.WriteUInt.assert_called_once_with(len(pickled), 32)
        g.net.WriteData.assert_called_once_with(pickled, len(pickled))
        g.net.SendToServer.assert_called_once()

    def test_to_lua(self, g):
        from gmod import realms

        realms.CLIENT = True
        realms.SERVER = False

        from gmod.net import send

        send('foo', 5, 6, handled_in_lua=True)

        g.net.Start.assert_called_once_with('foo')
        g.net.WriteType.assert_has_calls([call(5), call(6)])
        g.net.SendToServer.assert_called_once()
