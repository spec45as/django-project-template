bootstrap:
	pipenv install --dev
	mkdir -p ./var/{log,run,pid}
	touch ./var/{log,run,pid}/.gitkeep
	cp conf/local_settings.template src/{{ project_name }}/settings/local_"$USER".py
	cp conf/env.template conf/env

	echo 'Для запуска проекта осталось:'
	echo '1. отредактировать conf/env'
	echo '2. выполнить src/manage.py migrate'
	echo '3. выполнить src/manage.py runserver'
