from django.urls import path
from . import views

app_name = 'tags'


urlpatterns = [
    path('', views.TagListView.as_view(), name='tag_list'),
    path('<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
]
