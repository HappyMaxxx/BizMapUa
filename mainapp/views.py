from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin

from .forms import RegisterUserForm, LoginUserForm

from django.db import transaction
from django.contrib.auth.models import User
from .models import Region

from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(AccessMixin):
    login_url = reverse_lazy('auth')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mainapp/register.html'
    success_url = '/login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        if User.objects.filter(email=user.email).exists():
            form.add_error('email', "User with this email already exists")
            return self.form_invalid(form)
        
        user.save()

        login(self.request, user)
        return redirect('profile')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('auth')
    

def index(request):
    return render(request, 'mainapp/index.html')

@login_required
def profileview(request):
    return render(request, 'mainapp/profile.html')

def mapview(request):
    return render(request, 'mainapp/map.html')

def regionview(request, koatuu):
    region = Region.objects.get(koatuu=koatuu)

    data = {
        'region': region,
    }

    return render(request, 'mainapp/region.html', data)

def page_not_found(request, exception):
    return render(request, 'mainapp/404.html', exception)