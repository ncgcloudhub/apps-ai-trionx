# apps-ai-trionx
AI Applications


appsai/
    manage.py
    appsai/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    socialai/
        __init__.py
        admin.py
        apps.py
        models.py
        views.py
        urls.py
        templates/
            socialai/
                scrape_website.html
                scrape_result.html
                generate_content.html
                generate_result.html
                generate_tags.html
                generate_tags_result.html
        static/

# Run Migrations:
python manage.py migrate

# Start the development server:
python manage.py runserver

# Create a new Django app:
python manage.py startapp <app_name>

# Create a new Django superuser:
python manage.py createsuperuser

# Run tests for the Django app:
python manage.py test <app_name>

# Generate database schema migrations:
python manage.py makemigrations

# Apply database schema migrations:
python manage.py migrate

# Collect static files:
python manage.py collectstatic

# Access the Django shell:
python manage.py shell

##### 
