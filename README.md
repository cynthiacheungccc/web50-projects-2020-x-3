# Project 3

Web Programming with Python and JavaScript

## Technology stack

Python framework [Django](https://docs.djangoproject.com/en/2.0/)
UI framwork [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
Datebase [PostgreSQL](https://www.postgresql.org/docs/12/index.html)

## Breif description
* orders/admin.py for web admin site service
* orders/models.py for all model define for the website
* orders/views.py for Web page in this Django application that generally serves a specific function and has a specific template.
* orders/constant.py for common define for web application such as order completed email reminder template
* orders/urls.py for all available urls can be access for this web

## Personal touch
- site administrators to mark orders as complete and allowing users to see the status of their pending or completed orders
- supporting sending users a confirmation email once their purchase is complete

## Setup
* you should set the right `EMAIL_HOST` in the `pizza/settings.py` to enable email service for the web
* you should create at least one contact instance by web admin site.
* you should create at least one index shelf image instance by web admin site.