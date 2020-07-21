from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import status
from .models import *
from .serializers import *


class ArticleView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        articles = Article.objects.all()      
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})
    
    def post(self, request):
        user = request.user
        article = Article(author_id=user)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentArticleView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ArticleSerializer(article)
        return Response(data=serializer.data)
    
    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.user.id != article.author_id and not request.user.is_staff:
            data = {"failed": "You haven't right for doing this."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        operation = article.delete()
        if operation:
            data = {"success": "delete successfull"}
            return Response (data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
 
    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.user.id != article.author_id and not request.user.is_staff:
            data = {"failed": "You haven't right for doing this."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data)

    

class LoginView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)