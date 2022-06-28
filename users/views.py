from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic as generic_views

from .forms import SignupForm

def index(request):
    return render(request, 'index.html')

class LogoutView(auth_views.LogoutView):
    pass

class CustomLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'}
        )

class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class SignupView(generic_views.FormView):
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('courses:list_courses')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)