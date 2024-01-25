
""" Report Analysis FASTAPI """
import os
import json
from app.api.api_v1.endpoints.report_analysis.json2dict import json2dict
# from json2dict import json2dict
from app.api.api_v1.endpoints.report_analysis.report_data import report_data
# from report_data import report_data
import requests
from fastapi import FastAPI, HTTPException, status
from fastapi import APIRouter
# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.api_v1.endpoints.report_analysis.x_ai import x_ai
# from x_ai import x_ai
from app.api.api_v1.endpoints.report_analysis.idiq_report import report_data_idiq
# from idiq_report import report_data_idiq
from app.api.api_v1.endpoints.report_analysis.smart_summary import compare_account_history
# from smart_summary import compare_account_history



def standardize_dict_values(input_dict):
    # Find the minimum and maximum values in the dictionary
    min_value = min(input_dict.values())
    max_value = max(input_dict.values())
    
    # Calculate the range
    value_range = max_value - min_value
    
    # Standardize the values between -1 and 1
    standardized_dict = {}
    for key, value in input_dict.items():
        if value_range == 0:
            # Avoid division by zero if all values are the same
            standardized_value = 0
        else:
            standardized_value = -1 + 2 * (value - min_value) / value_range
        standardized_dict[key] = standardized_value
    
    return standardized_dict


def serialize_dict(weight):

    # Iterate through the items in the weight_trns dictionary
    for key, value in weight.items():
        # Check if the value is not JSON-serializable
        if not isinstance(value, (str, int, float, bool, list, dict)):
            # Convert non-serializable data to serializable types (e.g., lists)
            weight[key] = value.tolist() if hasattr(value, 'tolist') else str(value)

    return weight


router = APIRouter()
path = os.getcwd().replace("//", "/")

# app.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


def download_and_process_json(url):
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

        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to download JSON file. Status code: {response.status_code}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: Wrong URL provided")

@router.post("/smartcredit")
async def process_json(link: str):
    try:
        json_data = download_and_process_json(link)
        # print(json_data)
        # if not report.filename.endswith(".json"):
        #     raise HTTPException(status_code=400, detail="Invalid file format. Only JSON files are allowed.")

        # try:
        #     json_path = f"{path}/{report.filename}"
        #     with open(json_path, "wb") as f:
        #         f.write(report.file.read())

        # except Exception as e:
        #     raise HTTPException(status_code=500, detail="No file found: " + str(e))    

        try:
            print("entered 2nd try")
            try:
                trns, equif, exper = json2dict(json_data)
            except ImportError as e:
                print(e)
                print("1st exception")

            try:
                print("entered 2ndtry")
                # print(json_data)
                trns_rep, equif_rep, exp_rep = report_data(json_data)
            except ImportError as e:
                print("2ndException")
                print(e)


            try:
                print("entered 3rd try")
                weight_trns, weight_exp, weight_equif = x_ai(trns.copy(),exper.copy(),equif.copy())
            except Exception as e:
                print(e)

            if weight_trns != {}:
                weight_trns = standardize_dict_values(serialize_dict(weight_trns))
                weight_trns = dict(sorted(weight_trns.items(), key=lambda x:x[1]))

            if weight_equif != {}:
                weight_equif = standardize_dict_values(serialize_dict(weight_equif))
                weight_equif = dict(sorted(weight_equif.items(), key=lambda x:x[1]))

            if weight_exp != {}:
                weight_exp = standardize_dict_values(serialize_dict(weight_exp))
                weight_exp = dict(sorted(weight_exp.items(), key=lambda x:x[1]))


            weight ={
            "TransUnion": weight_trns, 
            "Experian": weight_exp, 
            "Equifax": weight_equif
            } 
            with open("D:/Codistan/codistan/CreditButterfly/scripts/actionplan/Weights.json", "w") as file:
                json.dump(weight, file)

            trns_rep['weights'] = weight_trns
            equif_rep['weights'] = weight_equif
            exp_rep['weights'] = weight_exp

            # return report analysis and shap values
            report = {
                "TransUnion": trns_rep,
                "Equifax": equif_rep,
                "Experian": exp_rep
            }

            return report
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error processing JSON data: " + str(e))
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error handling file upload: " + str(e))
    # finally:
    #     os.remove(json_path)


class InputData(BaseModel):
    old: dict
    new: dict

@router.post("/summary/smartcredit")
async def calculate(input_data: InputData):
    try:
        negative, deleted = compare_account_history(input_data.old, input_data.new)
        return {
            "result": {
            "Repaired" : negative,
            "Deleted" : deleted
        }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






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
        audit_data = report_data_idiq(data)  # transunion, experian, equifax
        return {
            "TransUnion": audit_data[0],
            "Equifax": audit_data[2],
            "Experian": audit_data[1]
        }
    except Exception as general_exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error: {general_exception}") from general_exception


