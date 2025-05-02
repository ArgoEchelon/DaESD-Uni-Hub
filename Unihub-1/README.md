# DaESD-Uni-Hub
Distributed and Enterprise Software Development group project about a university hub, or community system. 

Notes:

Create media folder at project root

Add a default.jpg and default_community.jpg

Change the DATABASES section in unihub/settings.py to use your host machine settings for MySQL

create a .env file containing database settings, Django superuser, and Django settings

To run, open a terminal at the project root folder and run docker-compose up 

To create an admin user, run the command docker-compose exec web python manage.py createsuperuser from a terminal in the project root folder.
