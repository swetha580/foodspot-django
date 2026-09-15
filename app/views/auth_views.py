from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from app.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('login')
