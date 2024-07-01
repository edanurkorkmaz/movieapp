from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
import json
import urllib.request
from django.contrib.auth.decorators import login_required
import requests
from movie.models import FavoriteMovies

import urllib.parse
import urllib.request
import json
from django.shortcuts import render


    
def index(request):
    data = {}

    if request.method == 'POST':
        movie_title = request.POST.get('movie_title', '')
        
        url = 'https://api.themoviedb.org/3/search/movie'
        api_key = 'c6cd9636380176a7b2bb697f0edc99e7'

        if movie_title:
            try:

                encoded_movie_title = urllib.parse.quote(movie_title)
                full_url = f'{url}?api_key={api_key}&query={encoded_movie_title}'
                

                response = urllib.request.urlopen(full_url)
                movie_data = json.loads(response.read())
                

                if movie_data.get('results'):

                    movie_info = movie_data['results'][0]
                    data = {
                        "title": movie_info['title'],
                        "release_date": movie_info['release_date'],
                        "overview": movie_info['overview'],
                        "poster_url": f"https://image.tmdb.org/t/p/w500/{movie_info['poster_path']}"
                    }
                else:
                    data = {"error": "Film bulunamadı."}
            except Exception as e:
                data = {"error": f"Hata oluştu: {str(e)}"}
        else:
            data = {"error": "Lütfen bir film adı girin."}

    return render(request, "index.html", data) 

def search_results(request):
    data = {}

    if request.method == 'POST':
        movie_title = request.POST.get('movie_title', '')
        
        url = 'https://api.themoviedb.org/3/search/movie'
        api_key = 'c6cd9636380176a7b2bb697f0edc99e7'

        if movie_title:
            try:

                encoded_movie_title = urllib.parse.quote(movie_title)
                full_url = f'{url}?api_key={api_key}&query={encoded_movie_title}'

                response = urllib.request.urlopen(full_url)
                movie_data = json.loads(response.read())
                

                if movie_data.get('results'):

                    movie_info = movie_data['results'][0]
                    data = {
                        "title": movie_info['title'],
                        "release_date": movie_info['release_date'],
                        "overview": movie_info['overview'],
                        "poster_url": f"https://image.tmdb.org/t/p/w500/{movie_info['poster_path']}"
                    }
                else:
                    data = {"error": "Film bulunamadı."}
            except Exception as e:
                data = {"error": f"Hata oluştu: {str(e)}"}
        else:
            data = {"error": "Lütfen bir film adı girin."}

    return render(request, "search_results.html", data) 


@login_required 
def add_film(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            FavoriteMovies.objects.create(user=request.user, title=title)
            return redirect('favori_film')
        else:
            return HttpResponseBadRequest("Film adı boş olamaz.")
    return render(request, 'add_film.html')


def favori_film(request):
    movies = FavoriteMovies.objects.filter(user=request.user)
    return render(request, 'favori_film.html', {'movies': movies})


def film_detay(request, film_id):
    api_url = f'https://api.themoviedb.org/3/movie/{film_id}'
    api_key = 'c6cd9636380176a7b2bb697f0edc99e7'
    params = {
        'api_key': api_key,
        'language': 'tr-TR',
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        film_data = response.json()
        context = {
            'title': film_data.get('title'),
            'release_date': film_data.get('release_date'),
            'overview': film_data.get('overview'),
        }
        return render(request, 'film_detay.html', context)
    else:
        error_message = "Film detayları alınamadı. API'de bir hata oluştu."
        return render(request, 'hata.html', {'error': error_message})

