from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import fitz  # PyMuPDF
import openai
import os
from dotenv import load_dotenv
import time

# Load environment variables from the .env file
load_dotenv()

#Vert's Open AI API
openai.api_key = os.getenv("OPENAI_KEY")

# Initialize the FastAPI app
router = APIRouter()

# app.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Define request body models using Pydantic
class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    address: str
    ssn: str
    dob: str

class BureauInfo(BaseModel):
    equifaxAddress: str
    experianAddress: str
    transunionAddress: str
    experian:list
    equifax:list
    transunion:list

class DisputeInfo(BaseModel):
    disputeInstruction: str
    disputeReason: str


# Specify the PDF file path
path = os.getcwd().replace("//", "/")
path += "/app/api/api_v1/endpoints/dispute_letter/McCarthy-Law-Dispute-Letter-Handbook (3).pdf"

pdf_file_path = path

# Function to extract text from a specific section of the PDF
def extract_section_text(doc, start_text, end_text):
    text = ""
    start_found = False
 
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
 
        if "Contents" in page_text:
            continue
        elif int(page_num) == 2:
            if start_text in page_text:
                start_found = True
                text += page_text.split(start_text, 1)[1]
 
            try:
                if end_text in text and start_found:
                    text = text.split(end_text,1)[0]  # Stop extracting text when reaching the end_text
                    break
            except:
                break
            
        elif int(page_num) > 2:
            if start_text in page_text:
                start_found = True
 
            try:
                if end_text in text and start_found:
                    text = text.split(end_text,1)[0]  # Stop extracting text when reaching the end_text
            except:
                pass
            
            if start_found and int(page_num) != 2:
                text += page_text
    return text.strip()

# Open the PDF file
pdf_document = fitz.open(pdf_file_path)

# Extract text from the "Dispute Letter Requirements" section only
requirements_text = extract_section_text(pdf_document, "I. \nDispute Letter Requirements:", "II. \nDispute Letter Tips:")
tips_text = extract_section_text(pdf_document,"II. \nDispute Letter Tips:","III. \nCRA Addresses:")
cra_adress_text = extract_section_text(pdf_document,"III. \nCRA Addresses:","")
language_text = extract_section_text(pdf_document,"IV. \nDispute Language Based on Error:","")




# Close the PDF document
pdf_document.close()



def generate_response(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1.2, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]



def generate_letter(personal_info: Dict, bureau_info: Dict, dispute: Dict) -> str:
    complete_requirements = generate_response(f"""You are an Dispute letter specialist that writes unique dipsute
                                              letters with the inforation provided by the user.

                                              This is my {personal_info} to use in salutaion and valediction
                                              of letter and the information to dispute 
                                              "Things to Dispute: 
                                              DisputeReason: {dispute['disputeReason']}
                                              DisputeInstruction: {dispute['disputeInstruction']}
                                              Equifax: {bureau_info['equifax']},
                                              Experian: {bureau_info['experian']},
                                              TransUnion: {bureau_info['transunion']},"
                                              
                                              create a unique dispute letter for me that I can send to 
                                              Equifax: {bureau_info['equifaxAddress']}, 
                                              Experian: { bureau_info['experianAddress']},
                                              TransUnion:{ bureau_info['transunionAddress']}

                                              follow these instructions while generating the letter:
                                              
                                              - Create one letter for all the disputes and bureaus
                                              - Use these requirements {requirements_text}, Tips  {tips_text},
                                              Bureau Addresses  {cra_adress_text}, and sample {language_text} for
                                              each dispute letter where they are appropriate.
                                              - Write the letter in the range of 150 to 200 words.
                                              - Also mention the FCRA or FDCP laws that would be used.                              
                                        """)

    time.sleep(10)
    return complete_requirements


# API endpoint to generate a dispute letter
@router.post("/generate-letter")
async def generate_dispute_letter(
    personal_info: PersonalInfo,
    bureau_info: BureauInfo,
    dispute_info: DisputeInfo,
):
    try:
        letter = generate_letter(personal_info.dict(), bureau_info.dict(), dispute_info.dict())
        # print(generate_response(f"Is the salutation info filled using my info {personal_info}? in this letter: {letter}"))
        
        # Split the letter into three parts using "Subject:" as the marker
        intro, part1 = letter.split("Subject")
        subject, outro = part1.split("Sincerely")

        # # Print the three parts
        # print("Intro:", intro.strip())
        # print("\nSubject:", "Subject" + subject.strip())  # Add "Subject:" back to the subject section
        # print("\nOutro:", "Sincerely" + outro.strip())

        return {
            "letter": {
                "complete_letter":letter,
                "intro": intro.strip() if intro else None,
                "subject" : "Subject" + subject.strip() if subject else None,
                "outro" : "Sincerely" + outro.strip() if outro else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)