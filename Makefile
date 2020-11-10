SHELL=/bin/bash
ENV=env
CFG=$(ENV)/pyvenv.cfg

help:
	@echo Avalable goals:
	@echo - help - print this message and exit
	@echo - prepare - install dependencies

install-packages:
	if [[ "$$(apt list --installed 2>/dev/null | grep -e '^python3-\(pip\|venv\)/' -c)" -lt "2" ]] ; then \
		echo 'Type you password to install missing packages or press ^C to cancel' ;\
		sudo apt install python3-pip python3-venv ;\
	fi


$(CFG) $(ENV): install-packages
	python3 -m venv $(ENV)

prepare: $(CFG)
	( \
		. $(ENV)/bin/activate; \
		pip3 install lxml bs4 pyyaml transliterate numpy pandas; \
	)
