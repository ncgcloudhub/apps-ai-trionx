# socialai/urls.py:

from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape_website, name='scrape_website'),
    path('generate/', views.generate_content, name='generate_content'),
    path('generate_tags/', views.generate_tags, name='generate_tags'),
    path('chat/', views.chat, name='chat'), 
    path('upload_file/', views.upload_file, name='upload_file'), 
]

