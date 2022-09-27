#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
# from cloudant.client import Cloudant - out-of-date
# from cloudant.error import CloudantException - out-of-date
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

import requests


def main(dict):
    database_name = "dealerships"

    print(dict)
    try:
        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])
    
        print("Databases:\n",service.get_all_dbs().get_result())
        print("Document? in " + database_name + ":\n", service.get_document(database_name,"1").get_result())
        
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
    print("No exceptions")
    return {"dbs": service.get_all_dbs().get_result()}
