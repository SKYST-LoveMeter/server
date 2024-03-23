FROM python:3.11

RUN echo "Django Project deploy 2024.02.13 00:32"

WORKDIR /home/

RUN git clone -b develop https://github.com/SKYST-LoveMeter/server.git

WORKDIR /home/server/

RUN pip install -r requirements.txt

RUN apt update

EXPOSE 8000

CMD ["bash", "-c", "git pull && python manage.py makemigrations --settings=config.settings.deploy && python manage.py migrate --settings=config.settings.deploy && gunicorn config.wsgi --env DJANGO_SETTINGS_MODULE=config.settings.deploy --bind 0.0.0.0:8000 --timeout 60"]