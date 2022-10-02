from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarModel,CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

GET_DEALERSHIP_URL = "https://us-east.functions.appdomain.cloud/api/v1/web/FSClouddkb_myCloudSpace/capstone/get_dealerships"
GET_DEALER_REVIEWS_URL = "https://us-east.functions.appdomain.cloud/api/v1/web/FSClouddkb_myCloudSpace/capstone/get_reviews"

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# `about` view 
def about(request):
    return render(request, 'djangoapp/about.html')



#  `contact` view
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = GET_DEALERSHIP_URL
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request,dealer_id):
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = GET_DEALER_REVIEWS_URL
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf( url, dealer_id )
        # Return a list of reviews
        return HttpResponse(dealer_reviews)





# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    
    # Check user authentication
    context = {}
    username = request.POST['username']
    password = request.POST['psw']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('djangoapp:index')
    else:
        context['message'] = "Invalid username or password."
        return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)
    
    review = {}
    # Test review 
    review["time"] = datetime.utcnow().isoformat()
    review["dealership"] = 11
    review["review"] = "This is a great car dealer"

    json_paload = {}
    json_payload["review"] = review

    response = post_request(url, json_payload, dealerId=dealer_id)

    #return render(request, , context)


