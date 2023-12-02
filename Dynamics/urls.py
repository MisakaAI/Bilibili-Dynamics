from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dynamics/", views.dynamics, name="dynamics"),
    path('dynamics/<int:class_id>/', views.dynamics, name='dynamics_class_id'),
]