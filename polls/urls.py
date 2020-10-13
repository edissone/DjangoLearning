from django.urls import path
from polls import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.ChoiceVoteView.as_view(), name='vote'),
    path('questions/', views.CreateQuestionFormView.as_view(), name='create_question'),
    path('<int:question_id>/comment/', views.CommentView.as_view(), name='create_comment')
]
