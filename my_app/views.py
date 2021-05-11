from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib import parse
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request: object):
    search = request.POST.get('search')
    #type(search) is a string, and can add the quote_plus towards it
    models.Search.objects.create(search=search) #the above search is what's going to be feed into the object, first search is param

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    #type(final_url) is also a string
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class':'result-row'})
    #print(post_titles[0]) #.text to get all the text of the titles; .get('href') to get the URLlink
    '''Don't need below now. But useful to the the render back at terminal about the returned info'''
    #post_title = post_listings[0].find(class_='result-title')
    #post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find(class_='result-price')
    #print(post_title,post_url,post_price)

    '''render to the front end now'''
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'): #can find
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_postings.append((post_title,post_url,post_price,post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings, #render returned results here
    }
    return render(request, 'my_app/new_search.html',stuff_for_frontend)