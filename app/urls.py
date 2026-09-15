from django.urls import path
from app.views import home, SignUpView

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
