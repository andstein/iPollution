

more information about the project on the
`make.opendata wiki <http://make.opendata.ch/doku.php?id=project:health:ipollution>`_


INSTALLATION (OS X, Linux)
--------------------------

  - (execute all following commands in the git repository)
  - install flask and PIL::

    virtualenv env
    source env/bin/activate
    pip install Flask pil

  - test your installation::

    python app/test.py

  - run the application::

    python app/main.py



INSTALLATION (Windows 7)
------------------------

  - install Python 2.7 from http://www.python.org/download/releases/2.7.3/
  
  - install easy_install as described here:
    http://flask.pocoo.org/docs/installation/#windows-easy-install

  - use easy_install to install PIP:
    to do this, open a Windows command prompt and execute  'easy_install pip'

  - use PIP to install FLASK and PIL:
    to do this, open a Windows command prompt and execute:
    pip install flask
    pip install pil
  
  - installing PIL may terminate on error message "error: Unable to find vcvarsall.bat"
    if this occurs, download a precompiled version PIL-fork-1.1.7.win-amd64-py2.7.exe from http://www.lfd.uci.edu/~gohlke/pythonlibs/
    and run this executable (installer file)
    
  - to test whether both have been successfully installed, start the Python GUI/Shell and enter
    import flask
    import Image
    (Note: if 'import Image' fails, try 'from PIL import Image')
    If Python accepts these commands without error message, flask and Image were successfully installed.
    
  - run the application:
    double-click on app\main.py



CONVERSION
----------

To calculate the pixels from the swiss coordinates, we use the following
approximation formula (this conversion is only valid for the provided
images!)::

	x_i = 1.4 * x_c - 658.2
	y_i = -1.42 * y_c + 423.32

Where ``x_i,y_i`` are the pixel coordinates and ``x_c/y_c`` the swiss coordinates
**divided by 1000** (i.e Bern is at 600/200).

