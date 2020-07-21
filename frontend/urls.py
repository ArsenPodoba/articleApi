from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('list/', artcileList, name='articleList'),
    path('article/<int:article_id>', article, name='article'),
    path('addnew/', addnew, name='addnew')
]