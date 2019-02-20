# DanceFloorV2

## Install Guide
Download and execute the latest Python 2.* installation package from https://www.python.org/downloads/windows/

NOTE - you have to use the command prompt (Win+R, cmd) *not bash*

Set system environment variables
```
- set PYTHON_HOME=C:\Python27
- set PATH=%PYTHON_HOME%\bin;%PYTHON_HOME%\Scripts\;%PATH%
```

If you have python 3 and python 2
```py -2 -m pip install virtualenv virtualenvwrapper-win```

If you have just python 2, the above will fail. Instead use:
```pip install virtualenv virtualenvwrapper-win```

At this point, `mkvirtualenv` should work - if not, close your command prompt and open it again in the right directory.
Second reminder - this only works with the command prompt, not bash.

```
mkvirtualenv -p C:\Python27\python.exe dance
pip install git+https://github.com/dpallot/simple-websocket-server.git
pip install flask
pip install flask-htpasswd
pip install pillow
pip install tweepy
deactivate
git clone git@github.com:PhilMarsden/DanceFloorV2.git
cd DanceFloorV2
copy flask_secret.dev flask_secret
```

See ``floor\processor\template.py`` for an example template for making a processor

# To work on the project
``workon dance``

``python floor\run-show.py --devserver``

http://localhost:1979

http://localhost:1977

## Authentication

If you want to access any of the protected endpoints locally, you'll need to specify a .htpasswd file.

The .htpasswd.dev file contains a user named "admin" with the password "password". For local development, you can just use this file, e.g.:

``cp .htpasswd.dev .htpasswd``
