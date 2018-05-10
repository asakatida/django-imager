# django-imager
**Author** : Adam Grandquist and Jay Adams
**Version**: 0.1.0
[![Coverage Status](https://coveralls.io/repos/github/jayadams011/django-imager/badge.svg?branch=master)](https://coveralls.io/github/jayadams011/django-imager?branch=master)

[![Build Status](https://travis-ci.org/jayadams011/django-imager.svg?branch=master)](https://travis-ci.org/jayadams011/django-imager)

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
* `./manage.py compilescss`
* `./manage.py collectstatic`
* `./manage.py check`
* `./manage.py test`
* `./manage.py runserver`


## Assets



## Architechture
Python 3.6
Django
bootstrap
venv
scss




## API
None at this time

## Change log
d9afbb3 finish adding scss functionality
f74ab28 added scss funtionality
9c8c3a4 fix content to context issue
51ae777 debug
46ba952 work on user added albums
601e7d8 migrated to a many to one albums
ac6a4e1 clean up debug
926bd7d work on forms
cec29fd work on forms
5ca5602 convert views to Template class
427fd44 Merge pull request #6 from jayadams011/class-33-tests
02d7bfc server setup
2e155c7 update and change enviornment
0d3acfa update and change enviornment
8d9b404 update and change enviornment
d469a17 update and change enviornment
2536c37 improve coverage
c886113 improve coverage
267ef65 improve coverage
9f5efac increase test coverage
a9d2693 add tests for views
59f859b setting up for RDS
77761e8 stash unneeded changes
1edd6c1 Merge pull request #5 from jayadams011/class-31-testing
f249ae7 fixed tests
9fda741 fixed tests
2c7aded fixed existing tests
8883539 fixed existing tests
c2d1a68 work on travis
1606786 working on travis
1bcb78e fix travis
d7f86c8 prep for travis
167d02a fix thumbnail to full on click
f071d22 add nav bar and buttons
78f084f fixed album and background to be dynamic
e61fcb2 fixing album view and cover views so if cover is none will have a cover
554dc8e fixed lightbox
5f419d4 working on lightbox
c36ea37 debug lightbox - still not perfect
429f223 Merge pull request #4 from jayadams011/class-29-views
a24467d add tests
b96c31c fix iamges for thumbnails
60e0fa6 added routes for albums and photos
1c2440e added context to library view
7964508 registered models
16b0704 added imports in views.py
302718f added signals.post in models.py
b3fe96d sliding sidebar css and js
f929fa9 added library and profile to menu
9a5399c added paths to urls and views for profiles, albums and photo
6f62e92 adding html to photo.html
bfe9539 modified library
0cecbc4 fill html in imager_profile
16cf49c scaffold
eb65c15 Merge pull request #3 from jayadams011/class-28-relationships
dcfceaa fixed readme and setup.congif
e3e17db added tests
5a1e029 added imager_images
0b42420 Merge pull request #2 from jayadams011/class-27-registration
4d8149e adding mkting text
0d117b3 updated readme.md
ce9eff6 added image top background....Salmon cookies rule
ac912b6 added bootstrap css
ac185c1 added login/logout
27a447a added comments
28858ec added registration.  Added test for registration
31877ee added test for home page
fb3888d adding home page
0167a7f cleaned up code as prpe for today
4301c47 Merge pull request #1 from jayadams011/class-26-profile
9badcba update readme.md
7278336 create model test
0c66caa installed multiselectfield
d47622e install fatory-boy, update requirements.txt
545bc70 changed all setting s to come form env
d271bda added models.py setup
115a2f9 created app imager_profile
06f0c77 create django app
61008d3 added readme and requirements.txt, set up env
86c0c96 updated gitignore
be8d0ee Initial commit
