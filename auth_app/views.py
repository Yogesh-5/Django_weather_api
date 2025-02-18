from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .models import cities
import requests
from .middleware import auth,guest

# Create your views here.


def home(request):
    return render(request,'auth_app/index.html')


@guest
def register_view(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        
    else:
        initial_data = {'username':'','password1':'','password2':''}
        form = UserCreationForm(initial = initial_data)
    return render(request, 'auth_app/register.html',{'form':form})    


@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
        
    else:
        initial_data = {'username':'','password':''}
        form = AuthenticationForm(initial = initial_data)
    return render(request, 'auth_app/login.html',{'form':form})    


@auth
def dashboard(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=f9861a93fcc63260924ff6b0c1981462'
    weather_data = []
    cities_list = cities.objects.all() 
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            add_city = cities.objects.create(city=city)
            add_city.save()
            return redirect('dashboard')
    for city in cities_list:
        get_weather = requests.get(url.format(city)).json()
        print(get_weather)
        weather = {
            'city':city,
            'temp': round((get_weather['main']['temp']-273.15),1),
            'desc': get_weather['weather'][0]['description'],
            'icon': get_weather['weather'][0]['icon'],
            'humidity': get_weather['main']['humidity'],
            'speed': get_weather['wind']['speed']
        }

        weather_data.append(weather)
    context = {'weather_data': weather_data}    


    return render(request, 'dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')




