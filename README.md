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

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/index.gif)

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/1.gif)

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/2.gif)

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/3.gif)

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/4.gif)

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/5.gif)

![index video](https://github.com/igokulganesh/Global-Industry/blob/master/Sample/6.gif)
