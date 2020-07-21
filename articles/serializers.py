from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'password'
        ]
        extra_kwargs = {
                    'password': {
                        'write_only': True
                        }
                    }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )


class UserLoginSerializer(serializers.ModelSerializer):

    token = serializers.CharField(read_only=True, allow_blank=True)
    email = serializers.EmailField(allow_blank=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {
                    'password': {
                        'write_only': True
                        },
                    'email': {
                        'write_only': True
                        }
                    }

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        password = data['password']
        if not email:
            raise ValidationError('A email is required')
        user = User.objects.get(email=email)
        if user:
            user_obj = user
        else:
            raise ValidationError('This email in not valid')
        
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorect credentials')
        
        data["token"], created = Token.objects.get_or_create(user=user)        
        return data


class ArticleSerializer(serializers.ModelSerializer):
    
    author_name = serializers.SerializerMethodField('get_author_name')

    def create(self, validated_data):
        return Article.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
            author_id=validated_data['author_id']
        )
    
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'text',
            'likes',
            'views',
            'author_name'
        ]
        extra_kwargs = {
            'author_name': {
               'read_only': True
                },
            'id': {
               'read_only': True
                },
            }
    
    def get_author_name(self, article):
        author_name = article.author_id.first_name + ' ' + article.author_id.last_name
        return author_name    