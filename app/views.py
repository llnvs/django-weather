import requests
from datetime import datetime
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    err_msg = ''
    message = ''
    message_class = ''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1864d344e8594dc173ad24e5b1e2fe4c'
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?cnt=24&q={}&units=metric&appid=1864d344e8594dc173ad24e5b1e2fe4c'
    print('<><><><><><>')
    aaa = requests.get(url2.format('London')).json()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existiong_city_counts = City.objects.filter(name=new_city).count()
            if existiong_city_counts == 0:
                response = requests.get(url.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                    return redirect('home')
                else:
                    err_msg = 'Could not find this city :('
            else:
                err_msg = 'City already exists !'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Success !'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    context = {
      'weather_data' : weather_data,
      'form': form,
      'message': message,
      'message_class': message_class
    }
    return render(request, 'weather.html', context)


def delete_city(request, city):
    City.objects.get(name=city).delete()
    return redirect('home')

def detail_city(request, city):
    city = City.objects.get(name=city)
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?cnt=24&q={}&units=metric&appid=1864d344e8594dc173ad24e5b1e2fe4c'

    forecast_response = requests.get(url2.format(city)).json()
    forecast = forecast_response['list']
    times = []
    temperatures = []
    for item in forecast:
        times.append(item['dt'])
        temperatures.append(item['main']['temp'])

    context = {
      'temperatures' : temperatures,
      'times': times,
      'city_name': city
    }
    return render(request, 'details.html', context)