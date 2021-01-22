from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('<int:pk>/question_rank/', views.QuestionRank.as_view(), name='question_rank'),
    path('<int:pk>/answer_create/', views.AnswerCreateView.as_view(), name='answer_create'),
    path('<int:pk>/<int:answer_pk>/', views.AnswerRank.as_view(), name='answer_rank'),
]
