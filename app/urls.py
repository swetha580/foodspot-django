from django.urls import path
from django.contrib.auth import views as auth_views
from app.views import home, signup, restaurant_list, restaurant_detail
from app.forms import StyledAuthenticationForm, StyledPasswordResetForm, StyledSetPasswordForm

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='app/login.html',
        authentication_form=StyledAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='app/password_reset.html',
        email_template_name='app/password_reset_email.html',
        subject_template_name='app/password_reset_subject.txt',
        form_class=StyledPasswordResetForm
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=StyledSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:pk>/', restaurant_detail, name='restaurant_detail'),
]
