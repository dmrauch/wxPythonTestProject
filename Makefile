pot:
	pygettext -a -d wxPythonTestProject -p locale wxPythonTestProject.py

mo:
	msgfmt locale/de/LC_MESSAGES/wxPythonTestProject.po -o locale/de/LC_MESSAGES/wxPythonTestProject.mo


dist:
	pyinstaller \
	--onefile \
	--clean \
	--log-level WARN \
	--key `cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1` \
	--add-data locale/de/LC_MESSAGES/wxPythonTestProject.mo:locale/de/LC_MESSAGES \
	--add-data graphics/flag_AF_30x20.bmp:graphics \
	--add-data graphics/flag_AF_30x20_disabled.bmp:graphics \
	--add-data graphics/flag_CO_30x20.bmp:graphics \
	--add-data graphics/flag_CO_30x20_disabled.bmp:graphics \
	--add-data graphics/flag_CZ_30x20.bmp:graphics \
	--add-data graphics/flag_CZ_30x20_disabled.bmp:graphics \
	--add-data graphics/flag_DE_33x20.bmp:graphics \
	--add-data graphics/flag_DE_33x20_disabled.bmp:graphics \
	--add-data graphics/flag_ES_30x20.bmp:graphics \
	--add-data graphics/flag_ES_30x20_disabled.bmp:graphics \
	--add-data graphics/flag_FR_30x20.bmp:graphics \
	--add-data graphics/flag_FR_30x20_disabled.bmp:graphics \
	--add-data graphics/flag_GB_40x20.bmp:graphics \
	--add-data graphics/flag_GB_40x20_disabled.bmp:graphics \
	--add-data graphics/flag_GR_30x20.bmp:graphics \
	--add-data graphics/flag_GR_30x20_disabled.bmp:graphics \
	--add-data graphics/flag_MX_35x20.bmp:graphics \
	--add-data graphics/flag_MX_35x20_disabled.bmp:graphics \
	--add-data graphics/flag_SE_32x20.bmp:graphics \
	--add-data graphics/flag_SE_32x20_disabled.bmp:graphics \
	--add-data graphics/flag_SK_30x20.bmp:graphics \
	--add-data graphics/flag_SK_30x20_disabled.bmp:graphics \
	--add-data graphics/fullscreen_34x24.bmp:graphics \
	--add-data graphics/Signal-Uncapped-t0obs.ico:graphics \
	--add-data graphics/transparent_1x1.bmp:graphics \
	wxPythonTestProject.py
	rm -f wxPythonTestProject.spec
	rm -rf build
