# Project-specific env variables
export DEBUG='true'
export SECRET_KEY='secret key'
export DB_NAME='imager'
export DB_USER='adam'
export DB_HOST='localhost'
export ALLOWED_HOSTS=''
export EMAIL_HOST=''
export EMAIL_PORT=''
export EMAIL_HOST_USER=''
export EMAIL_HOST_PASSWORD=''

source ENV/bin/activate.fish

imagersite/manage.py compilescss
imagersite/manage.py collectstatic
imagersite/manage.py makemigrations
imagersite/manage.py migrate
imagersite/manage.py runserver
