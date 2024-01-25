
""" FASTAPI for Getting Audit Data"""
import os
import json
from fastapi import FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
import requests
from app.api.api_v1.endpoints.audit.idiq_audit import get_audit_data
# from idiq_audit import get_audit_data
from app.api.api_v1.endpoints.audit.audit import json2dict
# from audit import json2dict


router = APIRouter()
path = os.getcwd().replace("//", "/")

# router.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

### url = """https://image.creditbutterfly.ai/creditreports/
#          64cc9b9bf32a64cfced273cc-64e33aef50f0b4bb6fb8d345.json"""


def download_and_process_json(url):
    """ 
    Get Json Data from Link

    Args:
        url: Json link

    Returns:
        Json : Credit report Json
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, timeout=10)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
             # Check if the response content type is JSON
            content_type = response.headers.get("content-type")
            # print(content_type)
            if content_type != "application/json":
                raise HTTPException(status_code=400,
                                     detail="The provided link does not point to a JSON file.")

            # Split the content into separate JSON objects
            json_objects = [line for line in response.text.splitlines()]

            # Initialize a list to store valid JSON objects
            valid_json_objects = []

            # Try to load each JSON object
            for json_str in json_objects:
                try:
                    json_data = json.loads(json_str)
                    valid_json_objects.append(json_data)
                except json.JSONDecodeError as json_error:
                    # Handle invalid JSON objects (corrupt)
                    print(f"Skipping invalid JSON object: {json_error}")

            if not valid_json_objects:
                raise HTTPException(status_code=400,
                                detail="No valid JSON objects found in the downloaded content.")

            if valid_json_objects:
                return valid_json_objects[0]
            else:
                raise HTTPException(status_code=400, detail="Received JSON is empty")

        else:
            raise HTTPException(status_code=response.status_code,
                 detail=f"Failed to download JSON file. Status code: {response.status_code}")

    except Exception as e:
        raise HTTPException(status_code=500,
                             detail="An error occurred: Wrong URL provided") from e

@router.post("/smartcredit")
async def process_json_smartcredit(link: str):
    """ 
    Getting Audit report from SmartCredit

    Args:
        data: Json Link from SmartCredit Paltform

    Returns:
        Json : Audit data from credit report
    """
    try:
        json_data = download_and_process_json(link)

        try:
            trns, equif, exper = json2dict(json_data)
            return {
                "TransUnion": trns,
                "Equifax": equif,
                "Experian": exper
            }
        except Exception as e:
            raise HTTPException(status_code=500,
                                 detail="Error processing JSON data: " + str(e)) from e

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error handling file upload: " + str(e)) from e



@router.post("/idiq")
async def process_json_idiq(data: dict):
    """ 
    Getting Audit report from IDIQ

    Args:
        data: Json Data from IDIQ Platform

    Returns:
        Json : Audit data from credit report
    """
    try:
        audit_data = get_audit_data(data)  # transunion, experian, equifax
        return {
            "TransUnion": audit_data[0],
            "Equifax": audit_data[2],
            "Experian": audit_data[1]
        }
    except Exception as general_exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Internal server error: {general_exception}") from general_exception
