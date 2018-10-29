Lua Reference
=============

You can interoperate with Python from Lua, for example, run arbitrary Python code.
All interop functions are in the ``py`` global table.

.. function:: py.Exec(code)

    Executes a string of Python code.

    ::

        py.Exec('print("HELLO".capitalize())')  -- Will print "Hello" to the console

Internal functions
------------------

These functions are used by GPython internally and not intended to be used by the regular addon developers.

.. function:: py._SwitchToClient()
              py._SwitchToServer()

    Switches to the GPython sub-interpreter which corresponds to the specified realm.
    Used primarily by the :mod:`gmod.hooks` module.
