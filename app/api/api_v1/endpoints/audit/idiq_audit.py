""" IdentityIQ Audit Data Cleaning """
import dataclasses
import json


@dataclasses.dataclass
class Bureau:
    """ Creating bureaus """
    def __init__(self) -> None:
        self.data = {
            "bureau" : '',
            "total_accounts" : 0,
            "delinquent_accounts" : 0,
            "derogatory_accounts" : 0,
            "no_of_collection" : 0, # No. of Unknowns
            "no_of_inq": 0,
            "no_of_pub_record": 0,
            "credit_score" : 0,
            "positive" : 0,
            "negative" : 0,
            "revolving_credit" : 0,
            "credit_card_balance" : 0,
            "late_pay" : 0,
            "inquiry" : [],
            "pub_record" : [],
            "derogatory" : []
        }

def creating_bureaus():
    """ 
    Creating the three Bureaus 

    Args:
        None

    Returns:
        bureau data :List of Bureaus data as TransUnion, Experian and Equifax
    """
    transunion = Bureau()
    transunion.data['bureau'] = 'TransUnion'

    experian = Bureau()
    experian.data['bureau'] = 'Experian'

    equifax = Bureau()
    equifax.data['bureau'] = 'Equifax'

    return [transunion.data, experian.data, equifax.data]


def get_summarized_data(bureau,data):
    """ 
    Getting Accounts summarized details

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing Accounts Summarized details.

    Returns:
        None
    """
    bureau['total_accounts'] = data['totalAccounts']
    bureau['delinquent_accounts'] = data['delinquent']
    bureau['derogatory_accounts'] = data['derogatory']
    bureau['no_of_collection'] = data['collection']
    bureau['no_of_inq'] = data['inquiries']
    bureau['no_of_pub_record'] = data['publicRecords']
    bureau['credit_score'] = data['creditScore']

def add_inquiries(bureau, data):
    """ 
    Getting Inquiries
    
    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing inquiries information.

    Returns:
        None
    """
    len_inq = len(data['creditorNames'])
    for i in range(len_inq):
        inquiry = {}
        if bureau['bureau'].lower() == data['creditBureaus'][i].lower():
            inquiry["inquirydate"] = data['inquiryDates'][i]
            inquiry["subscriber_name"] = data['creditorNames'][i]
            inquiry["business_type"] = data['businessTypes'][i]
        if inquiry:
            bureau['inquiry'].append(inquiry)


def add_pub_record(bureau, data):
    """ 
    Getting Public Record

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing public-record information.

    Returns:
        None
    """
    list_keys = data.keys()
    for key in list_keys:
        if key.lower() ==  bureau['bureau'].lower():
            len_pub_rec = len(data[key]['recordType'])
            for i in range(len_pub_rec):
                pub_rec = {}
                pub_rec['type'] = data[key]['recordType'][i]
                pub_rec['status'] = data[key]['recordStatuses'][i]
                pub_rec['date_filed'] = data[key]['filedDates'][i]
                pub_rec['reference_number'] = data[key]['recordReferences'][i]
                pub_rec['asset_amount'] = data[key]['recordAssetAmmounts'][i]
                try:
                    pub_rec['liability_amount'] = data[key]['recordLiabilities'][i]
                except KeyError:
                    pub_rec['liability_amount'] = data[key]['recordLiabilites'][i]
                pub_rec['exempt_amount'] = data[key]['recordExemptAmmounts'][i]
                pub_rec['court_name'] = data[key]['recordCourts'][i]
                bureau['pub_record'].append(pub_rec)

def get_pos_neg_acc(bureau, data):
    """
    Get Positive/Negative Accounts.

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing two-year payments information.

    Returns:
        None
    """
    neg_flags = ['30', '60', '90', '120', '150', '180', 'co', 'rf', 'pp', 'vs']

    if bureau['bureau'] == 'TransUnion':
        process_sublists(bureau, data['Transunion'], neg_flags)
    else:
        process_sublists(bureau, data[bureau['bureau']], neg_flags)

def process_sublists(bureau, sublists, neg_flags):
    """
    Process sublists to update positive and negative counters.

    Args:
        bureau (Bureau): The Bureau instance.
        sublists (list): List of sublists containing payment information.
        neg_flags (list): List of negative flags.

    Returns:
        None
    """
    for sublist in sublists:
        if any(flag in sublist for flag in neg_flags):
            bureau['negative'] += 1
        else:
            bureau['positive'] += 1

def get_credit_bal(bureau,data):
    """
    Getting Credit Limit and Revolving Balances

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing Credit Limit and Balances information.

    Returns:
        None
    """
    for i in range(len(data['balances'])):
        bureau['credit_card_balance'] += float(data['balances'][i].split("$")[1])
        bureau['revolving_credit'] += float(data['creditLimits'][i].split("$")[1])


def get_late_pay(bureau,data):
    """
    Get number of late payments

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing late payments information.

    Returns:
        None
    """
    late_flags = ['30', '60', '90', '120', '150', '180']

    if bureau['bureau'] == 'TransUnion':
        process_sublist_latepay(bureau, data['Transunion'], late_flags)
    else:
        process_sublist_latepay(bureau, data[bureau['bureau']], late_flags)

def process_sublist_latepay(bureau,sublist_bureau,late_flags):
    """
    processing sublist for latepay

    Args:
        bureau (Bureau): The Bureau instance.
        sublist_bureau (list): The data containing late payments information.
        late_flags: list of late flags which needs to be counted

    Returns:
        None
    """
    # Count occurrences of late flags in each sublist
    late_flags_count = sum(sublist.count(flag) for flag in late_flags
                            for sublist in sublist_bureau)

    bureau['late_pay'] = late_flags_count


def get_audit_data(file):
    """ 
    Getting Audit for reports 

    Args:
        None

    Returns:
        Audit data : Bureau's audit data as TransUnion, Experian and Equifax
    """
    aud_data = creating_bureaus() # transunion, experian, equifax
    bureaus_list = ['TransUnion', 'Experian', 'Equifax']

    # file = "D:/Codistan/codistan/CreditButterfly/scripts/ReportAnalysis/IdentityIQ/data.json"

    # with open(file, encoding="utf-8") as f:
    #     data = json.load(f)

    data = file  # Json Data file from DB

    for i, bureau in enumerate(aud_data):
        get_summarized_data(bureau, data[bureaus_list[i]])
        add_inquiries(bureau,data['inquiries'])
        add_pub_record(bureau,data['publicRecords'])
        get_pos_neg_acc(bureau,data[bureaus_list[i]]['accountsInformation']['twoYearPayments'])
        get_credit_bal(bureau,data[bureaus_list[i]]['accountsInformation'])
        get_late_pay(bureau, data[bureaus_list[i]]['accountsInformation']['twoYearPayments'])

    return aud_data
