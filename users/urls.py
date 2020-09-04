from django.urls import path
from users import views

urlpatterns = [
    path('<int:pk>/', views.UserProfileView.as_view(), name='profile'),
]
