from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import index, AuthView, AuthUpdateView

urlpatterns = [
    path('index', name='index', view=index),
    path('login', view=TokenObtainPairView.as_view()),
    path('refresh', view=TokenRefreshView.as_view()),
    path('new', view=AuthView.as_view()),
    path('update', view=AuthUpdateView.as_view())
]

