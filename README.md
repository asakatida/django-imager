# django-imager
**Author** : Adam Grandquist and Jay Adams
**Version**: 0.1.0

## Overview



## Getting Started
---------------
 Create an Imager clone for organizing and viewing artist protfolios and photos.  More features to come later....
*  Project-specific env variables
* `export SECRET_KEY='secret key'`
* `export DEBUG=True`
* `export DB_NAME='imager'`
* `export DB_USER=''` set these two if need for linux
* `export DB_PASSWORD=''`
* `export DB_HOST='localhost'` 

### initalize and run server

* `dropdb $DB_NAME`
* `createdb $DB_NAME`
* `./manage.py makemigrations`
* `./manage.py migrate`
* `./manage.py check`
* `./manage.py test`
* `./manage.py runserver`

## Assets



## Architechture
Python 3.6.4
Django
bootstrap
venv




## API
None at this time

## Change log
ce9eff6 (HEAD -> class-27-registration) added image top background....Salmon cookies rule
ac912b6 added bootstrap css
ac185c1 added login/logout
27a447a added comments
28858ec added registration.  Added test for registration
31877ee added test for home page
fb3888d adding home page
7278336 (HEAD -> class-26-profile) create model test
0c66caa installed multiselectfield
d47622e install fatory-boy, update requirements.txt
545bc70 changed all setting s to come form env
d271bda added models.py setup
115a2f9 created app imager_profile
06f0c77 create django app
61008d3 added readme and requirements.txt, set up env
86c0c96 (origin/master, origin/HEAD, master) updated gitignore
be8d0ee Initial commit

