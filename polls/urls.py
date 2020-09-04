from django.urls import path
from polls import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/', views.question_new, name='question_new'),
    path('questions/<int:question_id>/', views.add_choices, name='add_choices'),
]
