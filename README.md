# RestaurantLunchVoting
Company needs internal service for its’ employees which helps them to make a decision on lunch place. Each restaurant will be uploading menus using the system every day over API and employees will vote for menu before leaving for lunch.

# How to setup environment
* Open psql shell and run "setup_database.sql" to create database and user
    * Change user credentials and also correct those in settings.py
* Perform migration: python manage.py migrate
* Run "sql_pack.sql" to create database structure
* Create superuser: python manage.py createsuperuser

# How to run with Docker
* Navigate to your project dir
* Run: docker-compose up
    * It will run DB image, create required database with user, migrate and start project

**N.B.! You still need to run "sql_pack.sql" to create database structure in any preferred way.** 