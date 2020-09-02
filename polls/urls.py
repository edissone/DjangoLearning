from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('user/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('new/', views.question_new, name='question_new'),
    path('new/<int:question_id>/', views.add_choices, name='add_choices'),
]
