from django.urls import path
from django.contrib.auth import views as auth_views
from app.views import home, SignUpView

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='app/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
