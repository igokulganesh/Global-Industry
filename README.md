# Global Industry

This project’s main idea is to develop a system software for industries
through which they can manage operations based on the orders they get for
manufacturing their products. In every industry there is always waste of
time and human resources because of irregular management system. Using
this application, it would be easy for organizing it.

The Administrator or the Company technician will manage application
where he/she will daily update products list and employee list. He/ She will
update information of every available product in to database along with the
quantity of each product and as soon as the products are sold system will
automatically update the database.

# Requirements :

- download Postgresql and pgAdmin

- pip install Django

- pip install django-mathfilters

- pip install psycopg2

- pip install django-tenants

- pip install gunicorn whitenoise dj-database-url psycopg2

# How to run

1. create a database (same name as in settings.py)

2. Migrating schemas - python manage.py migrate_schemas

3. Create super user - python manage.py createsuperuser

4. Create public tenant - python manage.py create_tenant

   1. give schema name as 'public'
   2. give user as '1'
   3. domain - 'globalindustry.localhost'

5. python manage.py runserver

6. go to the url - http://globalindustry.localhost:8000/

# Samples

<img alt="0Sample" src="./Sample/index.gif">
<img alt="1Sample" src="./Sample/1.gif">
<img alt="2Sample" src="./Sample/2.gif">
<img alt="3Sample" src="./Sample/3.gif">
<img alt="4Sample" src="./Sample/4.gif">
<img alt="5Sample" src="./Sample/5.gif">
<img alt="6Sample" src="./Sample/6.gif">
