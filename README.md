# Task- Assignment

## Steps to set up the project:

### Manual setup

* create a python3.10 environment and activate it
* inside the main directory, create a .env file as follow and then edit the value according to the need
    >  .env
* install all the requirements 
    > pip install -r requirements.txt
* Please look into the accounts > models > auth.py , Please do the required changes as per 
  your project requirements, and then do the migrations
    > python manage.py makemigrations
* and now time to migrate the changes
    > python manage.py migrate
* then run the server
    > python manage.py runserver 
*create superuser
    > python manage.py cratesuperuser

** Using the admin credentials, generate an API token by hitting the /api/token endpoint to obtain a JWT token, and then use this token to access other APIs.
### Docker Setup in local machine

#### Create env file:-  
 create .env file parallel to .env_sample and change the values accordingly.

#### Install docker and docker composer:
[https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
###### 2: Local Environment
	docker-compose -f docker-compose.yml up -d --build

	Change database credential in .env file
	
	DB_NAME=postgres  
	DB_USERNAME=postgres  
	DB_PASSWORD=''  
	DB_HOST=db  
	DB_PORT=5432 

	Now you can access the server on 8004 port 
