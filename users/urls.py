from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('update/', views.UserUpdateView.as_view(), name='user_update'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
]

