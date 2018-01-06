# DanceFloorV2

Download and execute the latest Python 2.* installation package from https://www.python.org/downloads/windows/

Set system environment variables
- PYTHON_HOME = C:\Python27
- PATH : Add ;%PYTHON_HOME%\;%PYTHON_HOME%\Scripts\ 

Install Pip:

``pip install virtualenv``

``pip install virtualenvwrapper-win flask``
``pip install git+https://github.com/dpallot/simple-websocket-server.git``

``mkvirtualenv DanceFloorV2``

``deactivate``

``git clone git@github.com:PhilMarsden/DanceFloorV2.git``

``cd DanceFloorV2``

# To work on the project
``workon DanceFloorV2``

``python floor\run-show.py --driver devserver``

http://localhost:/1979
http://localhost:/1977
