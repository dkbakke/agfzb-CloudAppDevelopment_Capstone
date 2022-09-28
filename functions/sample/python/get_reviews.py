# get_reviews - intended for use in IBM Cloud Functions
# expects a dict with 'dealerId' and authentication paramaters
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
import requests


def main(dict):
    database_name = "reviews"
    doc_result =  {}
    try:
        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])
        my_selector =  {"dealership": dict["dealerId"]}      
        doc_result = service.post_find(db=database_name,selector=my_selector).get_result()
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
    return { "reviews" : doc_result["docs"] }
