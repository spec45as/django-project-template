install:
	pipenv install --python ~/.pythonz/pythons/CPython-3.6.0/bin/python --dev
	mkdir -p ./var/log
	mkdir -p ./var/pid
	mkdir -p ./var/run
	touch ./var/log/.gitkeep
	touch ./var/pid/.gitkeep
	touch ./var/run/.gitkeep
	cp conf/local_settings.template src/{{ project_name }}/settings/local_$(USER).py
	cp conf/env.template conf/env

	echo 'Для запуска проекта осталось:'
	echo '0. войти в виртуальное окружение: pipenv shell'
	echo '1. отредактировать conf/env'
	echo '2. выполнить src/manage.py migrate'
	echo '3. выполнить src/manage.py runserver'
