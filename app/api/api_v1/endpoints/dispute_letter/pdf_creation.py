data = {'Request for Correction of Personal Information': ['Incorrect Personal Information', 
        'Incorrect Personal Information', 'Incorrect Personal Information'], 
        'Dispute Regarding Duplicate Accounts': ['Duplicate Accounts', 'Duplicate Accounts', 
        'Duplicate Accounts'], 
        'Request to Update Account Status': ['Inaccurate Account Status', 'Inaccurate Account Status', 
        'Inaccurate Account Status'], 
        'Dispute of Fraudulent Accounts': ['Fraudulent Accounts', 'Fraudulent Accounts', 
        'Fraudulent Accounts'], 
        'Request for Removal of Outdated Account Information': ['Outdated Accounts', 'Outdated Accounts', 
        'Outdated Accounts'], 
        'Dispute of Incorrect Payment Status': ['Incorrect Payment Status', 'Incorrect Payment Status', 
        'Incorrect Payment Status'], 
        'Request to Remove Erroneous Late Payments': ['Erroneous Late Payments', 'Erroneous Late Payments',
        'Erroneous Late Payments'], 
        'Identity Theft Report and Dispute': ['Identity Theft', 'Identity Theft', 'Identity Theft'], 
        'Dispute of Unauthorized Credit Inquiries': ['Unauthorized Inquiries', 'Unauthorized Inquiries', 
        'Unauthorized Inquiries'],
        'Request for Correction of Account Mix-Up': ['Account Mix-Up', 'Account Mix-Up', 'Account Mix-Up']}


from fpdf import FPDF

class PDF(FPDF):
    # def header(self):
    #     self.set_font('Arial', 'B', 12)
    #     self.cell(0, 10, 'Letter', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

# Your letter content
letter = """Dear Sir/Madam: 
I am writing to dispute an unauthorized credit inquiry that was recently made on my credit report. I have been a victim of identity theft and suspect this inquiry is related to the incident. The inquiry was submitted by [Name of Credit Bureau], in which no authorization or permission has been given for such action. 

Please investigate this matter immediately, as it may be linked to fraudulent activity. As per the Fair Credit Reporting Act (FCRA), inquiries resulting from identity theft are not valid and must therefore be removed from my credit file promptly. Furthermore, any information obtained due to these illegal activities should also be deleted without delay.

I look forward to hearing back from you regarding your investigation into this issue at your earliest convenience so that we can resolve it quickly and protect my rights under FCRA laws governing consumer reporting agencies like yours. Thank you for taking the time out of your day to address this important matter with me today.

Sincerely,

[Your Signature]"""

letter2 = """Dear Sir/Madam: I am a victim of identity theft and I believe an account or accounts have been opened in my nathorization. Thithorization. This letter is to dispute the accuracy of this information as noted on your credit report, which was obtained from you on [date]. The following items are incorrect:
[list inaccurate items here]
This information has been reported inaccurately by [name of company], yet it still appears on my credit report. According to the Fair Credit Reporting Act (FCRA), Section 611(a)(1) requires that “all consumer reporting agencies must follow reasonable procedures to assure maximum possible accuracy” when compiling reports about consumers. Therefore, I request that you take immediate action to remove these entries from my credit report. Please provide written confirmation once this correction has been completed and all inaccurate records removed.
Thank you for your prompt attention to this matter. If there is anything else I can do please let me know.

Sincerely,
[Your Name]"""

pdf = PDF()
pdf.add_page()


pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'dispute', 0, 1, 'C')

pdf.set_font("Arial", size = 12)
# Calculate the maximum width for a line
max_line_width = pdf.w - 2*pdf.l_margin

# Split the letter content into lines that fit the width
lines = pdf.multi_cell(0, 10, letter.encode('latin-1', 'replace').decode('latin-1'))

pdf.add_page()
pdf.set_font("Arial", size = 12)

# Calculate the maximum width for a line
max_line_width = pdf.w - 2*pdf.l_margin

# Split the letter content into lines that fit the width
lines = pdf.multi_cell(0, 10, letter2.encode('latin-1','replace').decode('latin-1'))

pdf.output("data.pdf")
