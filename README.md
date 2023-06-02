Suade Labs Project


1) Clone the repo at the following link: https://github.com/joshua-malemba/SuadeLabs.git

After this, CD into the root directory. 

2) Assuming the db is holding data, feel free to remove it running the following cmd 

Windows: del db.sqlite3

Linux/Mac: rm db.sqlite3


After deleting the database file, you need to create a new, empty database file.

3) You can do this by running the following command in the project's root directory: python manage.py migrate


4) Finally, you can start the Django development server again using the following command:

python manage.py runserver

5) Implementation 

Open your preferred web browser and enter the following URL in the address bar:

http://localhost:8000/report/?date=<desired_date>

Replace <desired_date> with the date you want to generate the report for. 

For example, if you want to generate the report for AUGUST 25TH, 2019, you would use:

http://localhost:8000/report/?date=2019-08-25

The browser will send a request to the Django development server, 
which will generate the report for the specified date and return it as a JSON response.

Tests

Run: python manage.py test

