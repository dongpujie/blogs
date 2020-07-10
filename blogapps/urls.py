from django.urls import path

from . import views


app_name = 'blogapps'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='detail'),
]
