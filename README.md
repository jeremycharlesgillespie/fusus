# Dev Setup

Clone this project. Enter the `fusus` folder and run the following to stand up the containers:
```
docker-compose -f docker-compose.dev.yml up --build -d
```

Next run:
```
make setupdev
```
This will run `makemigrations`, `migrate`, and create the admin user that is defined in the .env.dev folder.

At this point the server is up and running and can be logged into with admin:admin. To test the API, use the associated 
Postman file or test independently.

# Prod Setup
Clone this project. Enter the `fusus` folder and run the following to stand up the containers:
```
docker-compose -f docker-compose.dev.yml up --build -d
```
The admin user must be made by hand. (Ideally this password would come from a method that is controlled by the CI/CD 
pipeline. Once the admin user account is complete, the password should be stored into a `secrets manager` for 
controlled access.)