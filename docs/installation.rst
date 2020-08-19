.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Alpha Shape Toolbox, run this command in your terminal:

.. code-block:: console

    $ pip install alphashape   

This is the preferred method to install Alpha Shape Toolbox, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Alternatively, if you make use of Anaconda for package installation and management, Alpha Shape can be installed from conda-forge:

.. code-block:: console

    $ conda install alphashape

Note you will receive a 'package not found error' if conda-forge has not already been added to your channels.
To add conda-forge:

.. code-block:: console

    $ conda config --add channels conda-forge
    $ conda config --set channel_priority strict

From sources
------------

The sources for Alpha Shape Toolbox can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/bellockk/alphashape

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/bellockk/alphashape/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/bellockk/alphashape
.. _tarball: https://github.com/bellockk/alphashape/tarball/master
