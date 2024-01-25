""" Creating ActionPlan """
import dataclasses
# import json
from datetime import datetime

@dataclasses.dataclass
class Bureau:
    """ Creating bureaus """
    def __init__(self) -> None:
        self.data = {
                "Bureau" : '',
                "Total Balances" : 0,
                "No of open Revolving Acc" : 0,
                "No of open Installment": 0,
                "No of open Collection Acc": 0,
                "Collection Details" : [],
                "Open Student loans" : 0,
                "Loan Details" : [],
                "Charge off" : [],
                "Bankruptcy": [],
                "Credit Limit" : 0,
                "Credit Score" : 0
            }

def creating_bureaus():
    """ Creating the three Bureaus """
    transunion = Bureau()
    transunion.data['Bureau'] = 'TransUnion'

    experian = Bureau()
    experian.data['Bureau'] = 'Experian'

    equifax = Bureau()
    equifax.data['Bureau'] = 'Equifax'

    return [transunion.data, experian.data, equifax.data]


def add_summary(bureau,data):
    """ Getting Account Details """
    # summary = {}
    bureau['Total Balances'] = data['balance']
    bureau['Credit Score'] = data['creditScore']
    # bureau['summary'] = summary
    credit = 0
    for _ , value  in enumerate(data['accountsInformation']['creditLimits']):
        credit += float(value.split("$")[1])
    bureau['Credit Limit'] = credit


def get_open_acc(bureau,data):
    """ Getting Open Acc """
    for i , val in enumerate(data['accountTypes']):
        if data['accountStatuses'][i].lower() == "open":
            if "revolving" in val.lower():
                bureau['No of open Revolving Acc'] += 1
            elif "installment" in val.lower():
                bureau['No of open Installment'] += 1
            elif "collection" in val.lower():
                bureau['No of open Collection Acc'] += 1
                temp_age = (datetime.strptime(data['lastReported'][i], "%m/%d/%Y")-
                                 datetime.strptime(data['dateOpened'][i], "%m/%d/%Y"))//365

                # Collection Details
                tmp_col = []
                tmp_col.append(temp_age)
                tmp_col.append(data['accountIds'][i])
                tmp_col.append(data['bankNames'][i])
                if data['accountStatuses'][i].lower() == "paid":
                    tmp_col.append("Paid")
                    bureau['Collection Details'].append(tmp_col)
        else:
            pass

        # Loan Details
        tmp = []
        tmp.append(data['comments'][i])
        tmp.append(data['balances'][i])
        tmp.append(data['accountIds'][i])
        tmp.append(data['twoYearPaymentsMonths'][i][-1])
        tmp.append(data['twoYearPaymentsYears'][i][-1])
        tmp.append(data['bankNames'][i])
        bureau['Loan Details'].append(tmp)

        # Charge off
        if 'chargeoff' in data['paymentStatuses'][i].lower() and data['balances'][i] != 0:
            tmp = []
            tmp.append(data['accountIds'][i])
            tmp.append(data['bankNames'][i])
            bureau['Charge off'].append(tmp)

        # Bankruptcy
        tmp_bnk = []
        if 'bankruptcy' in data['comments'][i]:
            tmp_bnk.append(data['accountIds'][i])
            tmp_bnk.append(data['bankNames'][i])
            tmp_bnk.append(data['lastReported'][i])
            bureau['Bankruptcy'].append(tmp_bnk)



def action_idiq(json_file):
    """
    Action Plan for IDIQ
    """
    repo_data = creating_bureaus() # transunion, experian, equifax
    bureaus_list = ['TransUnion', 'Experian', 'Equifax']

    # file = "D:/Codistan/codistan/CreditButterfly/scripts/actionplan/data.json"

    # with open(file, encoding="utf-8") as f:
    #     data = json.load(f)
    data = json_file

    for i, bureau in enumerate(repo_data):
        add_summary(bureau,data[bureaus_list[i]])
        get_open_acc(bureau,data[bureaus_list[i]]['accountsInformation'])

    return repo_data
