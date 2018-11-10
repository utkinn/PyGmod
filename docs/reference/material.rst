``material`` - ``Material`` class
=================================

.. automodule:: gmod.material
    :members:

Material parameters
-------------------

When creating a material from a PNG/JPG file, you can specify some parameters that will affect the material render
in different ways.

+---------------+----------------------------------------------------------------------+---------------------------------------------------+
| Parameter     | Explanation                                                          | Example                                           |
+===============+======================================================================+===================================================+
| ``NOCULL``    | This makes the back of the texture get drawn all the time.           | .. image:: material_params_examples/nocull.png    |
+---------------+----------------------------------------------------------------------+---------------------------------------------------+
| ``ALPHATEST`` |                                                                      | .. image:: material_params_examples/alphatest.png |
+---------------+----------------------------------------------------------------------+---------------------------------------------------+
| ``MIPS``      | This makes low-res versions of the texture that it swaps             | .. image:: material_params_examples/mips.png      |
|               | out as it gets smaller. It can help improve performance,             |                                                   |
|               | and you usually can't see the difference.                            |                                                   |
|               |                                                                      |                                                   |
|               | This can improve smoothing if you're scaling down the texture a lot. |                                                   |
+---------------+----------------------------------------------------------------------+---------------------------------------------------+
| ``NOCLAMP``   | This allows the texture to tile, so if you want a repeating pattern  | .. image:: material_params_examples/noclamp.png   |
|               | then it can help. It also stops the edges getting stretched, which   |                                                   |
|               | can make it look smoother.                                           |                                                   |
+---------------+----------------------------------------------------------------------+---------------------------------------------------+
| ``SMOOTH``    | This stops point sampling, which makes textures look like Minecraft. | .. image:: material_params_examples/smooth.png    |
|               | It makes the texture look smoother when you scale it.                |                                                   |
+---------------+----------------------------------------------------------------------+---------------------------------------------------+