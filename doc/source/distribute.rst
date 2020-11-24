Distributing the Application
============================

The goal is to provide the application in a way that is easy to distribute and install, i.e. users should ideally not have to set up a complicated environment and install a lot of dependencies. 
For commercial applications, the source code should be hidden and unreconstructable from the (binary) application - and of course, the license should permit the creation of non-free software.
Ideally, the same build tool or framework should be able to handle and deploy to different platforms.


PyInstaller
-----------

One tool which fulfills these criteria is PyInstaller. Given a Python script or module, it can identify all the dependencies and bundle them along with the program and Python itself either into a folder or, alternatively, into a single executable file (``--onefile``).

Additional data files can be attached using the ``--add-data`` flag. When building a single file, these data files are packed into the executable and extracted to a temporary folder during run time. This location can be retrieved using the ``sys._MEIPASS`` attribute. In the Python source code, something similar to the following snippet can be used to determine whether the current program instance is run from the source code by the interpreter or is run from a bundled distribution:

.. code:: python

  # special treatment of resource files for bundled application
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    self.graphicsPath = os.path.join(sys._MEIPASS, "graphics")
    self.localePath = os.path.join(sys._MEIPASS, "locale")
  else:
    self.graphicsPath = "graphics"
    self.localePath = "locale"

PyInstaller is not a cross-platform tool, i.e. it can only build distributions for the current platform. This means that for building distributions for different Python versions on the same OS, virtual environments have to be used, whereas virtual machines and containers can be used for building on different operating systems.

Resources:

- https://www.pyinstaller.org/
- https://pyinstaller.readthedocs.io/en/stable/index.html



Alternative Strategies
----------------------

- Embedding in C and compiling / bundling CPython with the application
- Cython creates equivalent C source files which can be compiled

Resources:

- https://python-compiler.com/post/how-to-distribute-python-program
- https://hackerboss.com/how-to-distribute-commercial-python-applications/
- https://docs.python.org/3/extending/embedding.html
- https://cython.org/
