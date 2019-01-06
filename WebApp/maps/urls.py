from django.conf.urls import url

from . import views

#^ from . (same directory) import views since we want to show the user the html response which will be in the view

urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
    url(r'search/', views.HomeView.as_view()),
]
