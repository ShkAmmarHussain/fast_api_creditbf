""" Creating Action Plan """

import json
import string
import dataclasses
from datetime import datetime
from app.api.api_v1.endpoints.actionplan_ratio.accnt import details
from app.api.api_v1.endpoints.actionplan_ratio.idiq_actionplan import action_idiq

# Given list of collection agencies
collection_agencies = [
    "Aargon Collection Agency",
    "Affiliated Management Services",
    "AFNI Collections Agency",
    "Bureau of Medical Economics",
    "Caine & Weiner Co",
    "Commonwealth Financial Systems",
    "Cavalry Portfolio Services",
    "Convergent Outsourcing",
    "Diversified Consultants",
    "DeVille Asset Management",
    "Enhanced Recovery Company",
    "EOS CCA",
    "Fidelity National Collections",
    "First Credit Services",
    "Hunter Warfield",
    "IC Systems",
    "Jefferson Capital Systems",
    "LVNV Funding",
    "Lamont, Hanley & Associates, Inc",
    "Midland Credit Management",
    "Midland Funding",
    "MARS Collection Agency",
    "Optimum Outcomes, Inc",
    "Portfolio Recover Associates",
    "Phoenix Financial Services, LLC",
    "Plaza Services LLC",
    "Resurgent Capital Services",
    "Stellar Recovery",
    "Source Receivables Management",
    "Thunderbird Collection Specialists",
    "Wakefield & Associates",
    "Williams & Fudge"
]

# Function to check if a name is present in the list
def is_name_in_list(name, agencies_list):
    # Convert both the input name and the names in the list to lowercase
    lowercase_name = name.lower()
    lowercase_agencies = [agency.lower() for agency in agencies_list]

    # Check if the lowercase input name is in the lowercase list
    return lowercase_name in lowercase_agencies

# # Example usage
# input_name = "Hunter Warfield"
# result = is_name_in_list(input_name, collection_agencies)

# if result:
#     print(f"{input_name} is present in the list.")
# else:
#     print(f"{input_name} is not present in the list.")




@dataclasses.dataclass
class Suggestion:
    """ Creating bureaus """
    def __init__(self) -> None:
        self.data = {
            "creditor" : "-",
            "acc_nmbr" : "-",
            "amount" : "-",
            "pay_stat" : "-",
            "instruction" : "-",
            "original_creditor" : "-",
            "type" : "-",
            "cards" : "-"
        }

def create_suggestion():
    """Empty Suggestion"""
    return Suggestion().data


# Step 2: Define a custom sorting function
def calculate_sentence_weight(sentence, weights):
    """ Calculating weignts according to AI Model """
    # print("error happened here")
    # Remove punctuation from the sentence
    sentence = sentence['instruction'].translate(str.maketrans('', '', string.punctuation))

    # Split the sentence into words
    words = sentence.split()

    # Initialize the total weight for the sentence
    total_weight = 2

    # Calculate the weight for the sentence by summing the weights of words in the dictionary
    for word in words:
        # print(word)
        if word.lower() in weights.keys():
          # print(word)
          # total_weight += weight_dict[word]
            total_weight =  weights[word.lower()]
    # print(total_weight)
    return total_weight

# Step 3: Define a sorting function that accepts weights as an argument
def custom_sort(sentences, weights):
    """ Sorting according to weights """
    # print('error happend at custom')
    return sorted(sentences, key=lambda sentence: calculate_sentence_weight(sentence, weights))

def action_plan(path_json,provider):
    """ Creating Action Plan """
    print("Endtered for actionplan")
    accounts = []
    # suggestions = {
    #     "TransUnion": None,
    #     "Experian" : None,
    #     "Equifax" : None
    # }
    suggestions = {
        "secured_card" : [],
        "student_loan" :[],
        "pay_settle" : [],
        "installment" : []
    }

    # Read json
    # with open("/home/ubuntu/actionplan/Weights.json",
    with open("D:/Codistan/codistan/CreditButterfly/scripts/actionplan/Weights.json",
              encoding = 'utf-8') as file:
        weights = json.load(file)
    print("got weights")

    if provider == "smartcredit":
        accounts =details(path_json)
    elif provider == "idiq":
        accounts = action_idiq(path_json)

    print("got accounts")

    #---------------------- Utilization Ratio ----------------------------#

    # balances, credit = 0, 0
    # try:
    #     for acc in accounts:
    #         balances += int(acc['Total Balances'])
    #         credit += int(acc['Credit Limit'])
    # except Exception:
    #     for acc in accounts:
    #         balances += float(acc['Total Balances'].replace("$","").replace(",",""))
    #         try:
    #             credit += float(acc['Credit Limit'].replace("$","").replace(",",""))
    #         except Exception:
    #             credit += float(acc['Credit Limit'])


    ## credit_weight, revolv_weight, instal_weight, collec_weight, public_weight = weights["Credit Limit"], weights["No of Revolving Acc"], weights["No of Installment"], weights["No of Collection Acc"], weights["No of Public Record"]
    ## print(f"{accounts}")

    ## print(f"{trns} /n {equ} /n {exp}")


    for accnt in accounts:
        tmp = []
        # if weights['Credit Limit'] < 0:

    #---------------------- Utilization Ratio ----------------------------#

        # if balances/credit > 0.3:
        #     tmp_sug = create_suggestion()
        #     tmp_sug["type"] = 'utilization_ratio'
        #     tmp_sug["instruction"] = 'Credit utilization is too high pay it down to 6%'
        #     tmp.append(tmp_sug)
        #     # tmp.append("Credit utilization is too high pay it down to 6%")
        # elif balances/credit < 0.06:
        #     tmp_sug = create_suggestion()
        #     tmp_sug["type"] = 'utilization_ratio'
        #     tmp_sug["instruction"] = 'Credit utilization is too low bring it up to 6%'
        #     tmp.append(tmp_sug)
        #     # tmp.append("Credit utilization is too low bring it up to 6%")

    #---------------------- RevolvingACC/ Card ----------------------------#

        if accnt['No of open Revolving Acc'] < 2:
            tmp_sug = create_suggestion()
            tmp_sug["type"] = 'revolving_account'
            if accnt['No of open Revolving Acc'] == 1:
                tmp_sug["instruction"] = 'Open one revolving account.'
                tmp_sug["cards"] = 1
            elif accnt['No of open Revolving Acc'] == 0:
                tmp_sug["instruction"] = 'Open two revolving account.'
                tmp_sug["cards"] = 2

            suggestions["secured_card"].append(tmp_sug)
            # tmp.append(tmp_sug)
            # tmp.append("Open revolving account should be at least 2.")

        if int(accnt['Credit Score']) <= 630:
            tmp_sug = create_suggestion()
            tmp_sug["cards"] = 1
            tmp_sug["instruction"] = 'Credit score is low Get a secured Credit card'
            # tmp.append(tmp_sug)
            suggestions["secured_card"].append(tmp_sug)
            # tmp.append("Credit score is low Get a secured Credit card")

        if 630 < int(accnt['Credit Score']) > 679:
            tmp_sug = create_suggestion()
            tmp_sug["cards"] = 1
            tmp_sug["instruction"] = 'Credit score is low Get a mid-tier unsecured credit card'
            suggestions["secured_card"].append(tmp_sug)
            # tmp.append("Credit score is low Get a mid-tier unsecured credit card")

    #---------------------- installment ----------------------------#

        if accnt['No of open Installment'] < 1:
            tmp_sug = create_suggestion()
            tmp_sug["type"] = 'installment_account'
            tmp_sug["instruction"] = 'Open at least 1 Installment Account'
            # tmp.append(tmp_sug)
            suggestions["installment"].append(tmp_sug)
            # tmp.append("Open at least 1 Installment Account")

    #---------------------- Student Loan ----------------------------#

        if len(accnt['Loan Details']) > 0:
            for a in accnt['Loan Details']:
                try:
                # Convert the date string to a datetime object
                    date_obj = datetime.strptime(a[3], "%Y-%m-%d")
                    if "student loan" in a[0]:
                        if 2020 < date_obj.year < 2023 and 3 < date_obj.month < 9:
                            tmp_sug = create_suggestion()
                            tmp_sug["type"] = 'student_loan'
                            tmp_sug["instruction"] = f'Inaccurate reporting of late payments for account {a[2]} send dispute to credit bureau.'
                            tmp_sug["amount"] = a[1]
                            tmp_sug["acc_nmbr"] = a[2]
                            tmp_sug["creditor"] = a[-1]
                            tmp_sug["pay_stat"] = a[-2]
                            suggestions["student_loan"].append(tmp_sug)
                            # tmp.append(tmp_sug)
                            # tmp.append(f"Inaccurate reporting of late payments for account {a[2]} send dispute to credit bureau")
                except Exception:
                    if "student loan" in a[0]:
                        datetime_object = datetime.strptime(a[-3], '%b')
                        numeric_month = datetime_object.month
                        if 20 < int(a[-2]) < 23 and 3 < numeric_month < 9:
                            tmp_sug["type"] = 'student_loan'
                            tmp_sug["instruction"] = f'Inaccurate reporting of late payments for account {a[2]} send dispute to credit bureau'
                            tmp_sug["amount"] = a[1]
                            tmp_sug["acc_nmbr"] = a[2]
                            tmp_sug["creditor"] = a[-1]
                            tmp_sug["pay_stat"] = a[-2]
                            suggestions["student_loan"].append(tmp_sug)
                            # tmp.append(tmp_sug)
                            # tmp.append(f"Inaccurate reporting of late payments for account {a[2]} send dispute to credit bureau")

                if "transferred" in a[0] and (a[1] == 0 or a[1] == "$0.00"):
                    tmp_sug = create_suggestion()
                    tmp_sug["type"] = 'transferred_account'
                    tmp_sug["instruction"] = f'Transferred accounts number: {a[2]}  should have a balance of 0'
                    tmp_sug["amount"] = a[1]
                    tmp_sug["acc_nmbr"] = a[2]
                    tmp_sug["creditor"] = a[-1]
                    tmp_sug["pay_stat"] = a[-2]
                    suggestions["student_loan"].append(tmp_sug)
                    # tmp.append(tmp_sug)
                    # tmp.append(f"Transferred accounts number: {a[2]}  should have a balance of 0")
                if any(item in a[0] for item in ["collection", "defaulted"]):
                    tmp_sug = create_suggestion()
                    tmp_sug["type"] = 'collection_account'
                    tmp_sug["instruction"] = 'Complete the REHAB program'
                    tmp_sug["amount"] = a[1]
                    tmp_sug["acc_nmbr"] = a[2]
                    tmp_sug["creditor"] = a[-1]
                    tmp_sug["pay_stat"] = a[-2]
                    suggestions["student_loan"].append(tmp_sug)
                    # tmp.append(tmp_sug)
                    # tmp.append("Complete the REHAB program")

    #---------------------- Pay ----------------------------#

        if len(accnt['Charge off']) > 0:
            for a in accnt['Charge off']:
                tmp_sug = create_suggestion()
                tmp_sug["type"] = 'charge_off'
                tmp_sug["instruction"] = f'Pay the charge off of account: {a[0]}'
                tmp_sug["acc_nmbr"] = a[0]
                tmp_sug["creditor"] = a[1]
                tmp_sug["pay_stat"] = a[2]
                tmp_sug["amount"] = a[3]
                suggestions["pay_settle"].append(tmp_sug)
                # tmp.append(tmp_sug)
                # tmp.append(f"Pay the charge off of account: {a}")

        if len(accnt["Collection Details"]) > 0:
            for a in accnt["Collection Details"]:
                tmp_sug = create_suggestion()
                tmp_sug["type"] = 'collection_account'
                tmp_sug["creditor"] = a[2]
                result = is_name_in_list(tmp_sug["creditor"], collection_agencies)

                if a[0] < 2 and result:
                    tmp_sug["instruction"] = f'Pay this collection account: {a[1]}'
                    # tmp.append(f"Pay this collection account: {a[1]}")
                elif a[0] > 2 and result:
                    tmp_sug["instruction"] = f'Pay this collection account: {a[1]} if collection agency agrees to delete this account'
                    # tmp.append(f"Pay this collection account: {a[1]} if collection agency agrees to delete this account")
                if 'Paid' in a[5]:
                    tmp_sug["instruction"] = f'Send a dispute for paid collection account: {a[1]}'
                    # tmp.append(f"Send a dispute for paid collection account: {a[1]}")

                tmp_sug["acc_nmbr"] = a[1]
                tmp_sug["creditor"] = a[2]
                tmp_sug["pay_stat"] = a[3]
                tmp_sug["amount"] = a[4]
                tmp_sug["original_creditor"] = a[6]
                if tmp_sug["instruction"] != "-":
                    suggestions["pay_settle"].append(tmp_sug)

    #---------------------- (Hasn't been changed yet) BankRuptcy ----------------------------#

        if len(accnt['Bankruptcy']) > 0:
            try:
                tmp_date = datetime.strptime(accnt['Bankruptcy'][0][-1], "%Y-%m-%d")
            except Exception:
                tmp_date = datetime.strptime(accnt['Bankruptcy'][0][-1], "%m/%d/%Y")
            tmp_acc = accnt['Bankruptcy'][0][0]
            tmp_sug = create_suggestion()
            tmp_sug["type"] = 'bankruptcy'
            for a in accnt['Bankruptcy']:
                try:
                    date_obj = datetime.strptime(a[-1], "%Y-%m-%d")
                except Exception:
                    try:
                        date_obj = datetime.strtime(a[-1], "%m/%d/%Y")
                    except Exception:
                        pass
                if date_obj >= tmp_date:
                    tmp_date = date_obj
                    tmp_acc = a[0]
                    tmp_bnk = a[1]
                if int(accnt['No of open Revolving Acc']) <= 0:
                    tmp_sug["instruction"] = 'Open a secured card due to bankruptcy as there are no open revolving accounts'
                    suggestions["secured_card"].append(tmp_sug)
                    # tmp.append("Open a secured card due to bankruptcy and no open revolving accounts")
                if int(accnt['No of open Installment']) <= 0:
                    tmp_sug["instruction"] = 'Open an installment account due to bankruptcy as there are no open installment accounts'
                    suggestions["installment"].append(tmp_sug)
                    ## tmp.append("Open an installment account due to bankruptcy and no open installment accounts")
            # tmp_sug["instruction"] = f"Settle all derogaroty accounts after Account:{tmp_acc} with bankruptcy date: {tmp_date}"
            # tmp_sug["acc_nmbr"] = tmp_acc
            # tmp_sug["creditor"] = tmp_bnk
            # suggestions["bankruptcy"].append(tmp_sug)
            ## tmp.append(tmp_sug)
            ## tmp.append(f"Settle all derogaroty accounts after Account:{tmp_acc} with bankruptcy date: {tmp_date}")


#---------------------- Sort Using Weights ----------------------------#

        # if accnt["Bureau"] == "TransUnion":
        #     weight = {
        #     'credit': weights["TransUnion"]["Credit Limit"],
        #     'revolving': weights["TransUnion"]["No of Revolving Acc"],
        #     'installment':  weights["TransUnion"]["No of Installment"],
        #     'collection':  weights["TransUnion"]["No of Collection Acc"],
        #     'bankruptcy':  weights["TransUnion"]["No of Public Record"],
        #     }

        #     sorted_tmp = custom_sort(tmp, weight)

        #     suggestions["TransUnion"] = sorted_tmp
        # elif accnt["Bureau"] == "Experian":
        #     weight = {
        #     'credit': weights["Experian"]["Credit Limit"], 
        #     'revolving': weights["Experian"]["No of Revolving Acc"],
        #     'installment':  weights["Experian"]["No of Installment"],
        #     'collection':  weights["Experian"]["No of Collection Acc"],
        #     'bankruptcy':  weights["Experian"]["No of Public Record"],
        #     }

        #     sorted_tmp = custom_sort(tmp, weight)

        #     suggestions["Experian"] = sorted_tmp
        # elif accnt["Bureau"] == "Equifax":
        #     weight = {
        #     'credit': weights["Equifax"]["Credit Limit"], 
        #     'revolving': weights["Equifax"]["No of Revolving Acc"],
        #     'installment':  weights["Equifax"]["No of Installment"],
        #     'collection':  weights["Equifax"]["No of Collection Acc"],
        #     'bankruptcy':  weights["Equifax"]["No of Public Record"],
        #     }

        #     sorted_tmp = custom_sort(tmp, weight)

        #     suggestions["Equifax"] = sorted_tmp

    return suggestions
    # print(suggestions)

# import json
# path_json = "D:/Codistan/codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/AAS MUNDY1.json"

# with open(path_json) as report:
#     report = json.load(report)

# print(action_plan(report,"smartcredit"))