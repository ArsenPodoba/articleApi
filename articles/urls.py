from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *


app_name = "articles"

urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('article/<int:pk>', CurrentArticleView.as_view()),
    path('user/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('getuser/', GetUserView.as_view()),
]