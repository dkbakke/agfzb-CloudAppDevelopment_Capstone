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
    try:
        if ( "api_key" in kwargs ):
            # Basic authentication GET
            api_key = kwargs["api_key"]
            response = requests.get(url, 
                headers={'Content-Type': 'application/json'},
                params=kwargs,
                auth=HTTPBasicAuth('apikey', api_key)
                )
        else:  
            # no authentication GET
            response = requests.get(url,
                headers={'Content-Type': 'application/json'},
                params=kwargs )
    except:
        # If any error occurs
        print("Network exception occurred")


    # TODO Need more error checking
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print( json_data )
    return json_data

    
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))
    response = {}
    
    try:
    # Call get method of requests library with URL and parameters
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

    ANALYZE_SENTIMENT_URL="https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/d30e1795-7de3-4ea9-ba4a-5707519aa8d1/v1/analyze"
    ANALYZE_SENTIMENT_API_KEY="<API-KEY>"
    NLU_VERSION="2022-04-07"
    NLU_FEATURES={                 
                    "keywords": 
                        {
                        "sentiment": True,
                        "limit": 1
                        }
                   
                }

    url=ANALYZE_SENTIMENT_URL
    api_key=ANALYZE_SENTIMENT_API_KEY
    # Call get_request with a URL parameter and api_key
    params = dict()
    params["text"] = review
    params["version"] = NLU_VERSION
    params["features"] = NLU_FEATURES
    #params["return_analyzed_text"] = ???
    json_result = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))

    print( json_result)
    return json_result
    



