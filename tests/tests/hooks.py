from unittest import TestCase
from unittest.mock import patch, Mock, call

from .table_mock import TableMock


def create_g_mock_empty_args():
    return TableMock({
        'CLIENT': True,
        '_py_hook_data': TableMock({}),
        '_py_n_data': 0,
        'py': TableMock({
            '_watched_events': TableMock({
                '_type_name_': b'table'  # TODO
            })
        })
    })


def create_g_mock_with_args():
    return TableMock({
        'CLIENT': True,
        '_py_hook_data': TableMock({
            1: 3, 2: 'boo', 3: TableMock({'i': 4})
        }),
        '_py_n_data': 3,
        'py': TableMock({
            '_watched_events': TableMock({
                '_type_name_': b'table'  # TODO
            })
        })
    })


class HookTestCase(TestCase):
    @patch('gmod.lua.G', new_callable=create_g_mock_empty_args)
    def test_normal_no_args(self, g):
        from gmod import hooks

        cb1 = Mock(name='hook_callback_1')
        cb2 = Mock(name='hook_callback_2')
        cbo = Mock(name='other_event_callback')

        cb1 = hooks.hook('Event1')(cb1)
        cb2 = hooks.hook('Event1')(cb2)
        cbo = hooks.hook('Event2')(cbo)

        hooks.event_occurred('Event1')

        cb1.assert_called_once_with()
        cb2.assert_called_once_with()
        cbo.assert_not_called()

    @patch('gmod.lua.G', new_callable=create_g_mock_with_args)
    def test_normal_with_args(self, g):
        from gmod import hooks

        cb1 = Mock(name='hook_callback_1')
        cb2 = Mock(name='hook_callback_2')
        cbo = Mock(name='other_event_callback')

        cb1 = hooks.hook('Event1')(cb1)
        cb2 = hooks.hook('Event1')(cb2)
        cbo = hooks.hook('Event2')(cbo)

        hooks.event_occurred('Event1')

        cb1.assert_called_once_with(3, 'boo', g['_py_hook_data'][3])
        cb2.assert_called_once_with(3, 'boo', g['_py_hook_data'][3])
        cbo.assert_not_called()

    @patch('gmod.lua.G', new_callable=create_g_mock_with_args)
    def test_normal_with_args_then_without_args(self, g):
        from gmod import hooks

        cb1 = Mock(name='hook_callback_1')
        cb2 = Mock(name='hook_callback_2')
        cbo = Mock(name='other_event_callback')

        py_hook_data_table_on_index_3 = g['_py_hook_data'][3]

        cb1 = hooks.hook('Event1')(cb1)
        cb2 = hooks.hook('Event1')(cb2)
        cbo = hooks.hook('Event2')(cbo)

        hooks.event_occurred('Event1')

        g['_py_hook_data'] = TableMock({})
        g['_py_n_data'] = 0

        hooks.event_occurred('Event1')

        cb1.assert_has_calls([call(3, 'boo', py_hook_data_table_on_index_3), call()])
        cb2.assert_has_calls([call(3, 'boo', py_hook_data_table_on_index_3), call()])
        cbo.assert_not_called()

    @patch('gmod.lua.G', new_callable=create_g_mock_with_args)
    def test_removal(self, g):
        from gmod import hooks

        func = Mock()
        cb = hooks.hook('a')(func)

        self.assertTrue(hasattr(cb, 'remove'))

        cb.remove()

        self.assertIs(func, cb)
        self.assertFalse(hasattr(cb, 'remove'))

    @patch('gmod.lua.G', new_callable=create_g_mock_with_args)
    def test_bad_event_type(self, g):
        from gmod import hooks

        cb = Mock()

        with self.assertRaises(TypeError):
            hooks.hook(1)(cb)
