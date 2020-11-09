ENV=env
CFG=$(ENV)/pyvenv.cfg

help:
	@echo Avalable goals:
	@echo - help - print this message and exit
	@echo - prepare - install depencies

$(CFG):
	python3 -m venv $(ENV)

activate: $(CFG)
	. $(ENV)/bin/activate

depencies: $(CFG)
	pip3 install lxml bs4 pyyaml transliterate

prepare: activate depencies
	@echo 'Done'
