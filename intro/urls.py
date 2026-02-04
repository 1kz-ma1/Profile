# intro/urls.py
from django.urls import path
from . import views

app_name = "intro"

urlpatterns = [
    path('', views.index, name='index'),                 # /
    path('about/', views.about, name='about'),           # /about/
    path('blog/', views.blog, name='blog'),              # /blog/
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),  # /blog/1/
    path('blog/<int:pk>/like/', views.like_post, name='like_post'),  # /blog/1/like/
    path('contact/', views.contact, name='contact'),     # /contact/
    path('portfolio/', views.portfolio, name='portfolio'),# /portfolio/
    path('thanks/', views.thanks, name='thanks'),        # /thanks/
    path('privacy/', views.privacy, name='privacy'),     # /privacy/
]