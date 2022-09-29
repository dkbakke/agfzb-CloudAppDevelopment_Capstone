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
        if ( "review" in dict ): 
            review = dict["review"]
        else:
            return { 
                "statusCode" : 500,
                 "error" : "No review provided"
                }
        response = service.post_document(db=database_name, document=review).get_result()
        print(response)     
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])
        return {
            "statusCode" : 500,
            "apiexception": ae.message
            }    
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {
            "statusCode" : 500,
            "error": err
            }
    if ( response["ok"] ):
        return { 
                "statusCode" : 200, 
                "response" : response
         }
