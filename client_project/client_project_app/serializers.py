
from rest_framework import serializers
from .models import Project, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login

#User    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)  
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        email = validated_data.pop('email') 
        user = User.objects.create_user(email=email, **validated_data)  
        return user
    
#Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        model = login
        fields = ['username','password']
        
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password')
        else:
            raise serializers.ValidationError('Username and password are required')

        attrs['user'] = user
        return attrs

#Project        
class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.client_name')  
    created_by = serializers.CharField(source='created_by.username')  
   
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'users', 'created_at', 'created_by']
        
        
        
    def update(self, instance, validated_data):
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
    
#Client
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name','projects', 'created_at', 'created_by']
        
    
    
#Client
class ClientupdateSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name','projects', 'created_at', 'created_by','updated_at']
        
    def update(self, instance, validated_data):
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.updated_at = timezone.now()
        instance.save()
        return instance


