import json
import requests
# from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi import APIRouter
from app.api.api_v1.endpoints.actionplan_ratio.u_ratio import ratio_data


router = APIRouter()

# Function to download and process a JSON file
def download_and_process_json(url):
    """
    Download Json Data from link
    """
    # url = "https://image.creditbutterfly.ai/creditreports/64cc9b9bf32a64cfced273cc-64e33aef50f0b4bb6fb8d345.json"

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
             # Check if the response content type is JSON
            content_type = response.headers.get("content-type")
            # print(content_type)
            if content_type != "application/json":
                raise HTTPException(status_code=400, detail="The provided link does not point to a JSON file.")

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
                raise HTTPException(status_code=400, detail="No valid JSON objects found in the downloaded content.")

            if valid_json_objects:
                return valid_json_objects[0]
            else:
                raise HTTPException(status_code=400, detail="Received JSON is empty")


            # Process the valid JSON objects
            # return valid_json_objects[0]

            # print("Downloaded JSON data:", json_objects[0])
            # if json_objects:
            #     return json_objects[0]
            # else:
            #     raise HTTPException(status_code=400, detail="Received JSON is empty")

            # return json_objects[0]
            # Process each JSON object individually
            # for json_data in json_objects:
            #     # Process the JSON data as needed
            #     print("Downloaded JSON data:", json_data)
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to download JSON file. Status code: {response.status_code}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: Wrong URL provided")


@router.post("/smartcredit")
async def process_ratio_smartcredit(link: str):
    """
    Endpoint to get Utilization Ratio
    """

    try:
        json_data = download_and_process_json(link)
        ratio = ratio_data(json_data,"smartcredit")
        # Check if personal_info is empty or corrupt
        # if not is_valid_personal_info(personal_info):
        #     raise HTTPException(status_code=400, detail="Invalid or empty personal info provided.")

        return {"ratio_data": ratio}

    except HTTPException as http_exception:
        return {"error": http_exception.detail}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@router.post("/idiq")
async def process_ratio_idiq(data: dict):
    """ 
    Getting Audit report from IDIQ

    Args:
        data: Json Data from IDIQ Platform

    Returns:
        Json : Audit data from credit report
    """
    try:
        ratio = ratio_data(data,"idiq")  # transunion, experian, equifax

        return {"ratio_data": ratio}

    except Exception as general_exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error: {general_exception}") from general_exception
