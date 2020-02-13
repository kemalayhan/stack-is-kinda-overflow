from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/answer_create', views.AnswerCreateView.as_view(), name='answer_create'),
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<int:pk>/update/', views.QuestinUpdateView.as_view(), name='question_update'),
]
