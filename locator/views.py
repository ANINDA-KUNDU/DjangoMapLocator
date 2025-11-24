from django.shortcuts import render, redirect
import folium
from .models import Search
from .forms import SearchForm
from django.http import HttpResponse
from geopy.geocoders import Nominatim
# Create your views here.


def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SearchForm()

    address = Search.objects.all().last()

    if not address:
        return HttpResponse("No address found. Please enter one.")

    geolocator = Nominatim(user_agent="django-map-app")
    location = geolocator.geocode(str(address))

    
    if location is None:
        address.delete()
        return HttpResponse("Could not find this location. Try another address.")

    lat = location.latitude
    lng = location.longitude
    country = location.address.split(',')[-1]

    map_obj = folium.Map(location=[lat, lng], zoom_start=6)
    folium.Marker([lat, lng], tooltip="Click", popup=country).add_to(map_obj)

    map_html = map_obj._repr_html_()

    return render(request, 'locator/home.html', {
        'map': map_html,
        'form': form
    })