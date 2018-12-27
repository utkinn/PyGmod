Lua Reference
=============

You can communicate with Python from Lua, for example, run arbitrary Python code.
All functions are in the ``py`` global table.

.. function:: py.Exec(code)

    Executes a string of Python code.

    ::

        py.Exec('print("HELLO".capitalize())')  -- Will print "Hello" to the console

Internal functions
------------------

These functions are used by PyGmod internally and not intended to be used by the regular addon developers.

.. function:: py._SwitchToClient()
              py._SwitchToServer()

    Switches to the PyGmod sub-interpreter which corresponds to the specified realm.
