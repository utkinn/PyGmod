Lua Reference
=============

You can communicate with Python from Lua, for example, run arbitrary Python code.
All functions are in the ``py`` global table.

.. function:: py.Exec(code)

    Executes a string of Python code.

    ::

        py.Exec('print("HELLO".capitalize())')  -- Will print "Hello" to the console

.. function:: py.Import(module)

    Imports a Python module and returns it.

    ::

        -- Print the Python version
        local sys = py.Import("sys")
        print(sys.version)
