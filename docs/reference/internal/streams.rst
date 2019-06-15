``pygmod._streams`` - I/O to Garry's Mod
========================================

Custom I/O classes which redirect I/O to the Garry's Mod console.

.. module:: pygmod._streams
    :synopsis: I/O to Garry's Mod

.. class:: GmodConsoleOutStream

    Base class for Garry's Mod console output streams.

.. class:: GmodConsoleOut

    Class which redirects the standard output (stdout) to the Garry's Mod console.

    Messages from the *client* realm are printed with the yellow color
    and messages from the *server* realm are printed with the blue color,
    just like ``print``, ``Msg`` and other Lua functions do.

    .. method:: write(s)

        Writes string ``s`` to Garry's Mod console with ``Msg`` Lua function.

.. class:: GmodConsoleErr

    Class which redirects the error output (stderr) to the Garry's Mod console.

    All messages are printed with the red color.

    .. method:: write(s)

        Writes string ``s`` to Garry's Mod console with ``MsgC`` Lua function with red color.

.. function:: setup()

    Sets :data:`sys.stdout` and :data:`sys.__stdout__` to a new :class:`GmodConsoleOut` instance
    and :data:`sys.stderr` and :data:`sys.__stderr__` to a new :class:`GmodConsoleErr` instance.
    Being called in ``main.cpp`` of the *C++* module, during the setup process.
