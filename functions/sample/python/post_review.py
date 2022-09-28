# post_review - IBM Cloud Function 

from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import requests

def main(dict):
    database_name = "reviews"
    try:
        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])
        if ( "review" not in dict ):
            review = { "review": 
                {   "id": "1114",
                    "name": "Upkar Lidder",
                    "dealership": 15,
                    "review": "Great service!",
                    "purchase": False,
                    "purchase_date": "02/16/2021",
                    "car_make": "Audi",
                    "car_model": "Car",
                    "car_year": 2021
                } 
            } 
        else: 
            review = dict

        review_doc = Document(
            id = review["review"]["id"],
            name = review["review"]["name"],
            dealership = review["review"]["dealership"],
            review =  review["review"]["review"],
            purchase = review["review"]["purchase"],
            purchase_date = review["review"]["purchase_date"],
            car_make = review["review"]["car_make"],
            car_model = review["review"]["car_model"],
            car_year = review["review"]["car_year"]
        )
        response = service.post_document(db=database_name, document=review_doc).get_result()
        print(response)     
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])
        return {"apiexception": ae.message}    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return { "response" : response }
