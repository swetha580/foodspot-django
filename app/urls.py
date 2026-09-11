from django.urls import path
from app.views import home, signup

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
]
