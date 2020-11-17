*************************
Introduction and Overview
*************************

.. include:: <isonum.txt>

This is a self-education project in order to revisit and get to know a few concepts and technologies. Therefore, the only point is to set up proofs of concept, whereas the actual content can be arbitrarily ridiculuous and nonsensical.


.. contents:: Table of Contents


Vision: Concepts and Technologies to Try Out
============================================

- **GUI**

  - *cross-platform capabilities*: The app should run on Linux, Windows, macOS and possibly mobile devices using Android and iOS
  - *single codebase*: All the different platforms should be supported with as little code and development duplication as possible
  - *translation readiness*: There should be a mechanism to provide translations for all the program components containing strings

- **Python**: Most of the application should be written in Python so as to benefit from high-level functionality and rapid development features

  - *Plug-in algorithms*: Compute-intensive tasks should be outsourced to performant algorithms written in C++ or NumPy/SciPy with defined interfaces which can be interchanged
  - *configuration management*: Via json

- **Web resources**: The application should be able to download and process online resources

- **Central server component**:

  - *REST API*: Should the client-server communication be based on a REST API?
  - *Encryption*: Both the server-side database as well as the communication between the server and client components should be encrypted
  - *Scope*: At first, the client-server communication should work in the local network, but eventually also over the internet or VPNs

- **Database**: The server component should have a central database which is accessed by the client application

  - Should local databases used for configuration management and translations in the client applications, rather than json files?

- **Web interface / application**: Can access the server and essentially do the same things as the native applications

- **Building, testing and deploying**

  - *source code management / version control*
  - *continuous delivery*
  - *unit and run-time tests*
  - *one-click deployment to all platforms*

- **Documentation**

  - *Sphinx*: for both manually written documentation pages and the auto-generated class/code reference

- **Commercial licensing**: Software components and technologies used should allow for commercial distribution



Tools and Technologies
======================

- **Python**: high-level programming language for rapid development

- **virtualenv**: python environment and package dependency and version management

- **wxPython**: cross-platform GUIs that can be written in Python

  - alternative options would be: *PySide2*/*PyQt5*, *kivy*

- **json**: configuration management

- **git**: version control

  - *GitHub*: Hosted git service, provides continuous delivery services

- **Sphinx**: documentation and automated source code / API reference

  - Read The Docs Sphinx theme

- **markdown**: documentation



Installation and Setup
======================

Go to some appropriate folder on your computer and clone the ``wxPythonTestProject`` `GitHub repository <https://github.com/dmrauch/wxPythonTestProject>`_:

.. code:: bash

  $ cd ~/Computing/Programming/wxPython
  $ git clone https://github.com/dmrauch/wxPythonTestProject.git

Enter the project folder and create a virtualenv:

.. code:: bash

  $ cd wxPythonTestProject
  $ virtualenv -p python3 env

Activate the environment with

.. code:: bash

  $ source env/bin/activate

The project root folder, i.e. in my case ``~/Computing/Programming/wxPython/wxPythonTestProject`` will be denoted by ``<wxPythonTestProject>`` in the rest of this documentation and, whenever the environment is activated, the command prompt will be prependet accordingly, i.e. ``(env) $``.


wxPython
--------

Now install `wxPython <https://pypi.org/project/wxPython/>`_ using ``pip``:

.. code:: bash

  $ pip install --upgrade pip   # possibly upgrade pip
  $ pip install wxPython

The appropriate precompiled wheels for you architecture and system may not be available, in which case ``pip`` will have to compile wxPython. This may take a few minutes.

In case the installation fails with the message

.. code:: text

  checking for GTK+ - version >= 3.0.0... Package gtk+-3.0 was not found in the pkg-config search path.

make sure that you have the GTK3 development files installed, e.g. for Linux Mint 18.3 which is based on Ubuntu 16.04 this means installing the package `libgtk-3-dev`. Make sure the packages listed in https://groups.google.com/g/wxpython-dev/c/Xu5QHBqMEc4 (or https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/) are installed on your system:

- ``python3.5-dev``
- ``libwebkitgtk-dev``
- ``libjpeg-dev``
- ``libnotify-dev``
- ``freeglut3-dev``
- ``libsdl1.2-dev``
- ``libgtk2.0-dev`` (was already installed before)
- ``libtiff-dev`` |rarr| ``libtiffxx5-dev`` (I also installed ``python-libtiff`` but this may not be necessary)
- ``libgstreamer-plugins-base0.10-dev``



Sphinx
------

In the active environment, do

.. code:: bash

  (env) $ pip install sphinx
  (env) $ pip install sphinx-rtd-theme   # install the Read the Docs Sphinx theme



Build and Run
=============


Application
-----------

To run the application, simply do

.. code:: bash

  (env) $ python wxPythonTestProject.py



Sphinx Documentation
--------------------

In the active environment, do

.. code:: bash

  (env) $ cd doc
  (env) $ make html

The html version of the documentation is then made available in ``doc/build/html/index.html``.
