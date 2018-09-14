``realms``: determining the current realm
=========================================

.. automodule:: gmod.realms
    :members:

    .. data:: CLIENT
              SERVER

        Realm checking boolean constants. On the *client*, the ``CLIENT`` is ``True`` and the ``SERVER`` is ``False``,
        and vice versa on the *server*.

    .. data:: REALM

        String constant: ``'server'`` on the *server* and ``'client'`` on the *client*.
