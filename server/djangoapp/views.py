from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .models import CarMake,CarModel,CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

GET_DEALERSHIP_URL = "https://us-east.functions.appdomain.cloud/api/v1/web/FSClouddkb_myCloudSpace/capstone/get_dealerships"
GET_DEALER_REVIEWS_URL = "https://us-east.functions.appdomain.cloud/api/v1/web/FSClouddkb_myCloudSpace/capstone/get_reviews"
ADD_REVIEW_URL = "https://us-east.functions.appdomain.cloud/api/v1/web/FSClouddkb_myCloudSpace/capstone/post_review"

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
    context = {}
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = GET_DEALERSHIP_URL
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealerships"] = dealerships
        #print( context )
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request,dealer_id,short_name):
    context = {}
    context["dealer_id"] = dealer_id
    context["short_name"] = short_name

    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url = GET_DEALER_REVIEWS_URL
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf( url, dealer_id )
        context["dealer_reviews"] = dealer_reviews
        # Return a list of reviews
        #print(context)
        return render(request, 'djangoapp/dealer_details.html', context)





# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id, short_name):
    
    if ( request.user.is_authenticated):
        review = {}        
        context = {}
        context["dealer_id"] = dealer_id
        context["short_name"] = short_name
        if ( request.method == "GET" ):
            #  query the cars with the dealer id to be reviewed. 
            
            car_models = CarModel.objects.filter(dealer_id=dealer_id)
            #get(dealer_id=dealer_id)
            print( car_models )
            context["cars"] = car_models
            # The queried cars will be used in the <select> dropdown.
            # append the queried cars into context
            #  call render method to render add_review.html.
            return render(request, 'djangoapp/add_review.html', context)


        if ( request.method == "POST" ):
            # update the json_payload["review"] to use the actual values obtained from the review form.
            # For review time,  use some datetime.utcnow().isoformat() to convert it into ISO format to be consistent with the format in
            # Cloudant. - For purchase, you may use car.year.strftime("%Y") to only get the year from the date field.
            # Update return statement to redirect user to the dealer details page once the review post is done for example.
            print( request.POST["content"])
            
            # Review text
            review["review"] = request.POST["content"]
            review["time"] = datetime.utcnow().isoformat()
            # Dealer ID
            review["dealer_id"] = dealer_id
            # Reviwer Name
            review["name"] = request.user.username
            # Purchase (boolean)
            review["purchase"] = False
            if "purchasecheck" in request.POST:
	                if request.POST["purchasecheck"] == 'on':
	                    review["purchase"] = True
            #Puchase date
            review["purchase_date"] = request.POST["purchasedate"]
            #Car make,model, year
            car_ID  = request.POST["car"]
            car = CarModel.objects.get(id=car_ID)
            print(car)
            review["car_make"] = car.model_make.make_name
            review["car_model"] = car.model_name
            review["car_year"] = car.model_year.strftime("%Y")
            print( review )

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id, short_name=short_name)


