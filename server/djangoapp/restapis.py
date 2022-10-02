import requests
import json
from .models import CarMake,CarModel,CarDealer,DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = {}
    api_key = kwargs["api_key"]
    try:
    # Call get method of requests library with URL and parameters
        if ( api_key ):
            # Basic authentication GET
            response = requests.get(url, 
                headers={'Content-Type': 'application/json'},
                params=kwargs,
                auth=HTTPBasicAuth('apikey', api_key)
                )
        else:
            # no authentication GET
            response = requests.get(url,
                 headers={'Content-Type': 'application/json'},
                params=kwargs
                )
    except:
        # If any error occurs
        print("Network exception occurred")
    # TODO Need more error checking
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

    
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))
    response = {}
    api_key = kwargs["api_key"]
    try:
    # Call get method of requests library with URL and parameters
        if ( api_key ):
            # Authenticated POST
            response = requests.post(url, 
                params=kwargs,
                json=json_payload,
                auth=HTTPBasicAuth('apikey', api_key)
                )
        else:
            # Not authenticated POST
            response = requests.post(url, 
                params=kwargs,
                json=json_payload
                )
    except:
        # If any error occurs
        print("Network exception occurred")
    # TODO Need more error checking
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print( json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealer_id)
    print( json_result)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(
                name=review_doc["name"],
                dealer_id=review_doc["dealership"],
                review=review_doc["review"],
                purchase=review_doc["purchase"],
                purchase_date=review_doc["purchase_date"],
                car_make = review_doc["car_make"],
                car_model = review_doc["car_model"],
                car_year = review_doc["car_year"],
                review_id = review_doc["id"],
                sentiment= analyze_review_sentiments(review_doc["review"])
            )
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(review):
    json_results = []
    # Call get_request with a URL parameter and api_key
    params = dict()
    params["text"] = review
    #params["version"] = kwargs["version"]
    #params["features"] = kwargs["features"]
    #params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    json_result = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))

    print( json_result)
    if json_result:
        # Get the sentiment of the review in json_result
        sentimnet_result = json_result
        
    return sentiment_result



