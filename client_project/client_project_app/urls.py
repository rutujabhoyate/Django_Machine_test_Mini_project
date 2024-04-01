

from django.urls import path
from .views import Clientdetails, Projectdetails, ClientdetailApiView, Projectdetails,ProjectdetailApiView,RegisterApiView,LoginApiView, LogoutApiView


urlpatterns = [
    
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('clients/',Clientdetails.as_view(), name="client"),
    path('clients/<int:id>/', ClientdetailApiView.as_view(), name='client-detail'),
    path('projects/',Projectdetails.as_view(), name="client"),
    path('projects/<int:id>/', ProjectdetailApiView.as_view(), name='project-detail'),
]

