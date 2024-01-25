import fitz  # PyMuPDF

# Specify the PDF file path
pdf_file_path = 'D:/Codistan/codistan/CreditButterfly/scripts/DisputeletterGeneration/McCarthy-Law-Dispute-Letter-Handbook (3).pdf'

# Function to extract text from a specific section of the PDF
def extract_section_text(doc, start_text, end_text):
    text = ""
    start_found = False
    # print(len(doc))
    for page_num in range(len(doc)):
        # print(page_num)
        # if int(page_num) == 2:
        page = doc.load_page(page_num)
        page_text = page.get_text()
        # print(page_text)

        if "Contents" in page_text:
            continue
        elif int(page_num) == 2:
            if start_text in page_text:
                start_found = True
                text += page_text.split(start_text, 1)[1]
                # print(text)

            try:
                if end_text in text and start_found:
                    text = text.split(end_text,1)[0]  # Stop extracting text when reaching the end_text
                    break
                    # print(text)
            except:
                break
            
            # if start_found and int(page_num) != 2:
            #     text += page_text
        elif int(page_num) > 2:
            if start_text in page_text:
                start_found = True
                # text += page_text.split(start_text, 1)[1]
                # print(text)

            try:
                if end_text in text and start_found:
                    text = text.split(end_text,1)[0]  # Stop extracting text when reaching the end_text
                    # print(text)
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

# print(language_text)


import pandas as pd
import os


path = os.getcwd().replace('\\','/')

# dispute_csv = 'D:/Codistan/CreditButterfly/scripts/disputeletter2csv/Dispute_letters.csv'
# df = pd.read_csv(dispute_csv)

personal_info = {
    "first_name" : "Ammar",
    "last_name" : "Hussian",
    "address" : "asacsfas",
    "ssn" : "13082738123",
    "dob" : "11/3/1239",
}

bureau_info = {
    "name" : "transunion",
    "address" : "uagdiavckabkfuauf"
}

disputes_and_letter_titles = {
    "Incorrect Personal Information": "Request for Correction of Personal Information",
    "Duplicate Accounts": "Dispute Regarding Duplicate Accounts",
#     "Inaccurate Account Status": "Request to Update Account Status",
#     "Fraudulent Accounts": "Dispute of Fraudulent Accounts",
#     "Outdated Accounts": "Request for Removal of Outdated Account Information",
#     "Incorrect Payment Status": "Dispute of Incorrect Payment Status",
#     "Erroneous Late Payments": "Request to Remove Erroneous Late Payments",
#     "Identity Theft": "Identity Theft Report and Dispute",
#     "Unauthorized Inquiries": "Dispute of Unauthorized Credit Inquiries",
#     "Account Mix-Up": "Request for Correction of Account Mix-Up",
}


import random
import openai

#Vert's Open AI API
openai.api_key = "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"




def generate_response(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1.2, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


generated_letters = {}

import time
for dispute, letter_title in disputes_and_letter_titles.items():
    letter = []
    complete_requirements = generate_response(f"""Hi this is my {personal_info}
                                                create a unique dispute letter for me that I can send to {bureau_info}
                                                according to the given context in the triple back ticks below.

                                                follow these instructions while generating the letter:
                                                
                                                - Use these requirements {requirements_text}, Tips  {tips_text},
                                                Bureau Addresses  {cra_adress_text}, and sample {language_text} for
                                                each dispute letter where they are appropriate.
                                                - Write the letter in the range of 150 to 200 words.
                                                - Also mention the FCRA or FDCP laws that would be used.
                                                                                        
                                                ```{dispute}```                                     
                                        """)
    letter.append(complete_requirements)
    time.sleep(10)
    generated_letters[letter_title] = letter



from fpdf import FPDF 

class PDF(FPDF):
    # def header(self):
    #     self.set_font('Arial', 'B', 12)
    #     self.cell(0, 10, 'Letter', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


pdf = FPDF() 

for key,values in generated_letters.items():
    pdf.add_page() 
    
    # pdf.set_font("Arial", size = 12) 
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, key, 0, 1, 'C')

    i = 1
    for value in values:
        pdf.set_font("Arial", size = 12)
        # Calculate the maximum width for a line
        max_line_width = pdf.w - 2*pdf.l_margin
        # Split the letter content into lines that fit the width
        lines = pdf.multi_cell(0, 10, value.encode('latin-1', 'replace').decode('latin-1'))
        if i < 3:
            pdf.add_page()
        i += 1
    
pdf.output("AI_PDF.pdf") 