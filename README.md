# webllisto


Webllisto Employee Management System
==================================================

Getting Started
----------------

1. Create Python virtual environment:

        python3.6 -m venv .venv

2. Activate the virtual environment:

        source .venv/bin/activate

3. install  the project requirements:
	
		pip install -r requirements.txt 

4. Apply migrations

		./manage.py makemigrations
    
        ./manage.py migrate

5. To run the server:

        ./manage.py runserver
