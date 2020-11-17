# GUI Test Project with Python and wxPython

## Content

- [Vision: Concepts and Technologies to Try Out](#1-vision-concepts-and-technologies-to-try-out-[&#129045;])
- [Technologies Used](#2-technologies-used-[&#129045;])
- [Installation](#3-installation-[&#129045;])
  - [wxPython](#3.1-wxpython-[&#129045;])
  - [Sphinx](#3.2-sphinx-[&#129045;])
- [Build](#4-build-[&#129045;])


<br/>

## 1. Vision: Concepts and Technologies to Try Out [[&#129045;](#gui-test-project-with-python-and-wxpython)]

- **GUI**
  - &#9989; *cross-platform capabilities*: The app should run on Linux, Windows, macOS and possibly mobile devices using Android and iOS
  - &#9989; *single code base*: All the different platforms should be supported with as little code and development duplication as possible
  - *translation readiness*: There should be a mechanism to provide 
- **Python**: Most of the application should be written in Python so as to benefit from high-level functionality and rapid development features
  - *Plug-in algorithms*: Compute-intensive tasks should be outsourced to performant algorithms written in C++ or numpy/scipy with defined interfaces which can be interchanged
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


<br/>

## 2. Technologies Used [[&#129045;](#gui-test-project-with-python-and-wxpython)]

- **Python**: high-level programming language for rapid development
- **virtualenv**: python environment and package dependency and version management
- **wxPython**: cross-platform GUIs that can be written in Python (other options: PySide2/PyQt5, kivy)
  - Homepage: https://wxpython.org/
  - PyPI project page: https://pypi.org/project/wxPython/
  - API documentation: https://docs.wxpython.org/
    - Stock icons and bitmaps: https://wxpython.org/Phoenix/docs/html/stock_items.html
  - Wiki: https://wiki.wxpython.org/
    - Getting started: https://wiki.wxpython.org/Getting%20Started
    - List of events: https://wiki.wxpython.org/ListOfEvents
- **json**: configuration management
- **git**: version control
- **Sphinx**: documentation
  - Read The Docs theme: https://sphinxthemes.com/themes/read-the-docs (because it includes a drop-down list for the different versions)
- **markdown**: documentation


<br/>

## 3. Installation [[&#129045;](#gui-test-project-with-python-and-wxpython)]

TODO: Clone the repository from GitHub


Enter the project folder and in that folder create a virtualenv, e.g. like this:

    $ cd ~/Computing/Programming/wxPython/wxPythonTestProject
    $ virtualenv -p python3 env

To activate the environment, do

    $ source env/bin/activate


<br/>

### 3.1. wxPython [[&#129045;](#gui-test-project-with-python-and-wxpython)]

Now install wxPython (https://pypi.org/project/wxPython/)

    $ pip install wxPython

In case the installation fails with the message

    checking for GTK+ - version >= 3.0.0... Package gtk+-3.0 was not found in the pkg-config search path.

make sure that you have the GTK3 development files installed, e.g. for Linux Mint 18.3 which is based on Ubuntu 16.04 this means installing the package `libgtk-3-dev`. Make sure the packages listed in https://groups.google.com/g/wxpython-dev/c/Xu5QHBqMEc4 (or https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/) are installed on your system:

- `python3.5-dev`
- `libwebkitgtk-dev`
- `libjpeg-dev`
- `libnotify-dev`
- `freeglut3-dev`
- `libsdl1.2-dev`
- `libgtk2.0-dev` (already installed before)
- `libtiff-dev` &#10142; `libtiffxx5-dev` (also installed `python-libtiff`)
- `libgstreamer-plugins-base0.10-dev`


<br/>

### 3.2. Sphinx [[&#129045;](#gui-test-project-with-python-and-wxpython)]


<br/>

## 4. Build [[&#129045;](#gui-test-project-with-python-and-wxpython)]
