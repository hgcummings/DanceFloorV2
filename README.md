# DanceFloorV2

Download and execute the latest Python 2.* installation package from https://www.python.org/downloads/windows/

Set system environment variables
- set PYTHON_HOME=C:\Python27
- set PATH=%PYTHON_HOME%\bin;%PYTHON_HOME%\Scripts\;%PATH%

Install Pip:

``pip install virtualenv virtualenvwrapper-win flask ``

``pip install git+https://github.com/dpallot/simple-websocket-server.git``

``mkvirtualenv dance``

``deactivate``

``git clone git@github.com:PhilMarsden/DanceFloorV2.git``

``cd DanceFloorV2``

# To work on the project
``workon dance``

``python floor\run-show.py --devserver``

http://localhost:1979
http://localhost:1977
