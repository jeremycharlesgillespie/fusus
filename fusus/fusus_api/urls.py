from django.urls import path

from . import views

app_name = "Fusus API"

urlpatterns = [
    path('test/', views.Test.as_view(), name='fusus-api-test')
]
