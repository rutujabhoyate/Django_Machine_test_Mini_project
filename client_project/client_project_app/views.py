from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Client, Project
from .serializers import ClientSerializer,ProjectSerializer ,UserSerializer,LoginSerializer,ClientupdateSerializer
from django.contrib.auth import login as django_login, logout as django_logout,authenticate
from django.contrib.auth.models import User


########### USER ###########
#User|Register|Login|Logout

class RegisterApiView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user:
                django_login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed('Invalid credentials')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    def post(self, request):
        django_logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    

############ Client #############
#GET_ALL/PUT/POST/DELETE/GET BY ID 
class Clientdetails(APIView):
    
    def get(self, request):
        obj = Client.objects.all()
        serializer = ClientSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ClientdetailApiView(APIView):
    
    def get(self, request, id):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            msg = {"message": "Not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientupdateSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK) 
   

    def put(self, request, id,):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            msg = {"message":"Client Not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientupdateSerializer(client,data = request.data)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            client= Client.objects.get(id=id)
        except Client.DoesNotExist:
            msg = {"message": "Client not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
    
        serializer = ClientupdateSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

    def delete(self, request, id):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            msg = {"message":"Client Not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        client.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)
            
        
############ PROJECT ##################   
#GET_ALL|POST|PUT|PATCH|DELETE|GET_BY_ID            

class Projectdetails(APIView):
    
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        project_name = request.data.get('project_name')
        client_id = request.data.get('client_id')
        user_ids = request.data.get('users')
   
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(id__in=user_ids)
        project = Project.objects.create(project_name=project_name, client=client, created_by=request.user)
        project.users.set(users)
        serializer = ProjectSerializer(project)
        response_data = serializer.data
       
        return Response(response_data, status=status.HTTP_201_CREATED)
   
class ProjectdetailApiView(APIView):
    
    def get(self, request, id):
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            msg = {"message": "Project Not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)   

    def put(self, request, id,):
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            msg = {"message":"Project Not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, id):
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            msg = {"message": "Project not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
    
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

    def delete(self, request, id):
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist: 
            msg = {"message":"Project Not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        project.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)    
    
    
    
    
