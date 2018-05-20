# Project-specific env variables
export SECRET_KEY='secret key'
export DB_NAME='imager'
export DB_USER='grandquista'
export DB_PASSWORD='gYS-PUz-8SQ-924'
export DB_HOST='django-imager-db.cq1xm3hzsgz3.us-west-1.rds.amazonaws.com'
export ALLOWED_HOSTS='.amazonaws.com localhost'
export EMAIL_HOST=''
export EMAIL_PORT=''
export EMAIL_HOST_USER=''
export EMAIL_HOST_PASSWORD=''

source ENV/bin/activate.fish

ansible-playbook -i hosts playbooks/simple-playbook.yml -v
