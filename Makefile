ENV=env
CFG=$(ENV)/pyvenv.cfg

help:
	@echo Avalable goals:
	@echo - help - print this message and exit
	@echo - prepare - install depencies

$(CFG):
	python3 -m venv $(ENV)

prepare: $(CFG)
	PKG_COUNT=`apt list --installed 2>/dev/null | grep -e '^python3-\(pip\|venv\)/' -c`
	if [ $$PKG_COUNT -lt 2 ]; then \
		echo 'Type you password to install missing packages or press ^C to cancel' ;\
		sudo apt install python3-pip python3-venv ;\
	fi
	( \
		. $(ENV)/bin/activate; \
		pip3 install lxml bs4 pyyaml transliterate; \
	)
