
INSTALL
-------


  - install flask and PIL::
    virtualenv env
    source env/bin/activate
    pip install Flask pil
  - test your installation::
    python app/test.py




CONVERSION
----------
To calculate the pixels from the swiss coordinates, we use the following approximation formula:

	x_i = 1.4 * x_c - 658.2
	y_i = -1.42 * y_c + 423.32

Where x_i,y_i are the pixel coordinates and x_c/y_c the swiss coordinates divided by 1000. (I.e Bern is at 600/200).
