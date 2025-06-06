from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import AccessMixin

from .forms import RegisterUserForm, LoginUserForm, BuisnesCreationForm

from django.db import transaction
from django.contrib.auth.models import User
from .models import Region, Businesse, BuisnessePhoto, Evaluation

from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

import json

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
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
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
    businesses = Businesse.objects.filter(region=region, status='added')

    sort_by = request.GET.get('sort_by', '')
    category = request.GET.get('category', '')
    city = request.GET.get('city', '')
    tag = request.GET.get('tag', '')

    if sort_by == 'popularity_desc':
        businesses = businesses.order_by('-average_rating')
    elif sort_by == 'popularity_asc':
        businesses = businesses.order_by('average_rating')
    if category:
        businesses = businesses.filter(category=category)
    if city:
        businesses = businesses.filter(city=city)
    if tag:
        businesses = businesses.filter(tags__contains=tag)

    count = len(Businesse.objects.filter(region=region, status='added'))

    categories = Businesse.objects.filter(region=region, status='added').values('category').distinct()
    cities = Businesse.objects.filter(region=region, status='added').values('city').distinct()
    tags = set()
    for business in businesses:
        if business.tags:
            tags.update(tag.strip() for tag in business.tags.split(' '))

    data = {
        'region': region,
        'businesses': businesses,
        'count': count,
        'categories': categories,
        'cities': cities,
        'tags': tags,
        'current_sort': sort_by,
        'category': category,
        'city': city,
        'tag': tag,
        'koatuu': koatuu,
    }

    return render(request, 'mainapp/region.html', data)

@login_required
def create_business(request):
    if request.method == 'POST':
        form = BuisnesCreationForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            
            photos = request.FILES.getlist('photos')
            for photo in photos:
                if isinstance(photo, UploadedFile):
                    BuisnessePhoto.objects.create(
                        businesse=business,
                        img=photo
                    )
            
            return redirect('home')
    else:
        form = BuisnesCreationForm()
    
    return render(request, 'mainapp/create_business.html', {'form': form})

def adminpanelview(request):
    if request.user.is_staff:

        try:
            pending_buisneses = Businesse.objects.filter(status='pending')
        except:
            pending_buisneses = []

        data = {
            'pending_buisneses': pending_buisneses
        }

        return render(request, 'mainapp/adminpanel.html', data)

def approve_buisnes(request, bisnes_id):
    bisnes = Businesse.objects.get(id=bisnes_id)
    bisnes.status = 'added'
    bisnes.save()

    return redirect('adminpanel')

def decline_buisnes(request, bisnes_id):
    bisnes = Businesse.objects.get(id=bisnes_id)
    bisnes.delete()

    return redirect('adminpanel')

@login_required
@csrf_protect
def rate_business(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        rating = request.POST.get('rating')
        
        try:
            business = Businesse.objects.get(id=business_id)
            rating = float(rating)
            if not 1 <= rating <= 5:
                return JsonResponse({'success': False, 'error': 'Оцінка повинна бути від 1 до 5'}, status=400)

            evaluation, created = Evaluation.objects.update_or_create(
                user=request.user,
                business=business,
                defaults={'rating': int(rating)}
            )
            business.update_average_rating()

            return JsonResponse({
                'success': True,
                'new_average_rating': business.average_rating
            })
        except Businesse.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Бізнес не знайдено'}, status=404)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Невалідна оцінка'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Невалідний метод запиту'}, status=400)

def buisnesview(request, buisnes_id):
    try:
        busines = Businesse.objects.get(id=buisnes_id)
    except:
        return redirect('404')
    
    data = {
        'busines': busines,
    }

    return render(request, 'mainapp/buisnes.html', data)

def my_bisneses(request):
    try:
        buisneses = Businesse.objects.filter(user=request.user)
    except:
        buisneses = []


    data = {
        'buisneses': buisneses
    }

    return render(request, 'mainapp/my_profiles.html', data)

def check_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        user = User.objects.filter(username=username).first()
        if username and user:
            return JsonResponse({'error': 'This username is already taken.'}, status=200)

        return JsonResponse({'error': ''}, status=200)

def page_not_found(request, exception):
    return render(request, 'mainapp/404.html', exception)

def server_error(request):
    return render(request, 'mainapp/404.html', status=500)