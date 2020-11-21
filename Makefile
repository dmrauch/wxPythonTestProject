pot:
	pygettext -a -d wxPythonTestProject -p locale wxPythonTestProject.py

mo:
	msgfmt locale/de/LC_MESSAGES/wxPythonTestProject.po -o locale/de/LC_MESSAGES/wxPythonTestProject.mo
