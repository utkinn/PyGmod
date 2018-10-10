from unittest import TestCase
from unittest.mock import patch, MagicMock
import pickle

from .table_mock import TableMock
import luastack

luastack.IN_GMOD = True


def create_g_mock():
    return TableMock({
        'net': TableMock({
            'Start': MagicMock(name='net.Start'),
            'WriteUInt': MagicMock(name='net.WriteUInt'),
            'WriteData': MagicMock(name='net.WriteData'),
            'Send': MagicMock(name='net.Send'),
            'SendToServer': MagicMock(name='net.SendToServer'),
        }),
        'Player': MagicMock(name='Player')
    })


@patch('gmod.lua.G', new_callable=create_g_mock)
class SendTestCase(TestCase):
    def test_wrong_message_type_name(self, g):
        g.CLIENT = False
        g.SERVER = True

        from gmod.net import send
        from gmod import player

        with self.assertRaises(TypeError):
            send(123, 1)

    def test_send_from_client(self, g):
        g.CLIENT = True
        g.SERVER = False

        from gmod.net import send
        from gmod import player

        data = (1, 2, 3)
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

        send('spam', *data)

        g.net.Start.assert_called_once_with('spam')
        g.net.WriteUInt.assert_called_once_with(len(pickled), 32)
        g.net.WriteData.assert_called_once_with(pickled, len(pickled))
        g.net.SendToServer.assert_called_once()

    def test_send_from_server(self, g):
        g.CLIENT = True
        g.SERVER = False

        from gmod.net import send
        from gmod import player

        data = (2, 3, 4)
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

        send('eggs', *data, receiver=player.get_by_userid(1))
