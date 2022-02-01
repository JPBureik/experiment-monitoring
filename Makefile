# setup:
#	 ./setup.sh

venv/bin/activate:
	/usr/bin/python3 -m pip install virtualenv
	/usr/bin/python3 -m virtualenv venv
	source ./venv/bin/activate