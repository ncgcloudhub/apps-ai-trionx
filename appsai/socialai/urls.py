# socialai/urls.py:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL pattern
    path('chat/', views.chat, name='chat'),
    path('scrape/', views.scrape_website, name='scrape_website'),
    path('generate/', views.generate_content, name='generate_content'),
    path('generate_tags/', views.generate_tags, name='generate_tags'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('contact/', views.contact, name='contact'),
    path('youtube/title-generator/', views.youtube_title_generator, name='youtube_title_generator'),
    path('youtube/tags-generator/', views.youtube_tags_generator, name='youtube_tags_generator'),
    path('youtube/description-generator/', views.youtube_description_generator, name='youtube_description_generator'),
    path('tiktok/title-generator/', views.tiktok_title_generator, name='tiktok_title_generator'),
    path('tiktok/tags-generator/', views.tiktok_tags_generator, name='tiktok_tags_generator'),
    path('tiktok/description-generator/', views.tiktok_description_generator, name='tiktok_description_generator'),
    path('facebook/title-generator/', views.facebook_title_generator, name='facebook_title_generator'),
    path('facebook/tags-generator/', views.facebook_tags_generator, name='facebook_tags_generator'),
    path('facebook/description-generator/', views.facebook_description_generator, name='facebook_description_generator'),
    path('instagram/title-generator/', views.instagram_title_generator, name='instagram_title_generator'),
    path('instagram/tags-generator/', views.instagram_tags_generator, name='instagram_tags_generator'),
    path('instagram/description-generator/', views.instagram_description_generator, name='instagram_description_generator'),
    path('content-writer/blog-title-generator/', views.blog_title_generator, name='blog_title_generator'),
    path('content-writer/blog-introduction/', views.blog_introduction_generator, name='blog_introduction_generator'),
    path('content-writer/blog-conclusion/', views.blog_conclusion_generator, name='blog_conclusion_generator'),
    path('content-writer/blog-body/', views.blog_body_generator, name='blog_body_generator'),
    path('content-writer/blog-tags-generator/', views.blog_tags_generator, name='blog_tags_generator'),
    path('vlog/title-generator/', views.vlog_title_generator, name='vlog_title_generator'),
    path('vlog/tags-generator/', views.vlog_tags_generator, name='vlog_tags_generator'),
    path('vlog/description-generator/', views.vlog_description_generator, name='vlog_description_generator'),
]
