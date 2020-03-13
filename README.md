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
    
# Description of API:
**Example usage of API**

_You can use any preferred tool to test API, my one is HTTPie (https://httpie.org)_
http http://127.0.0.1:8000/api/login/ username=a password=a 
http http://127.0.0.1:8000/api/create_restaurant/?name=r1 'Authorization: Token "put_authorization_token_here"'
http http://127.0.0.1:8000/api/hello/ 'Authorization: Token "put_authorization_token_here"'
http --form http://127.0.0.1:8000/api/upload_menu/ menu_file@D:\Development\python\RestaurantLunchVoting\menu_files\menu4.csv 'Authorization: Token "put_authorization_token_here"'		
http http://127.0.0.1:8000/api/add_employee/ name=c password=c 'Authorization: Token "put_authorization_token_here"'
http http://127.0.0.1:8000/api/current_day_menu/ 'Authorization: Token "put_authorization_token_here"'
http http://127.0.0.1:8000/api/vote/?restaurant=r3 'Authorization: Token "put_authorization_token_here"'
http http://127.0.0.1:8000/api/logout/ 'Authorization: Token "put_authorization_token_here"'