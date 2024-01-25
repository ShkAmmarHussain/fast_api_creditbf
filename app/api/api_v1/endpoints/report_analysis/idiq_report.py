""" IdentityIQ Report Data Cleaning """
import dataclasses
import json


@dataclasses.dataclass
class Bureau:
    """ Creating bureaus """
    def __init__(self) -> None:
        self.data = {
        "bureau" : '',
        "name" : '',
        "also_known_as": '',
        "c_address" : '',
        "p_address" : '',
        "c_employer" : '',
        "p_employer" : '',
        "birth_year" : '',
        "credit_score" : 0,
        "positive" : 0,
        "negative" : 0,
        "account_history" : {},
        "inquiry" : [],
        "pub_record" : [],
        "derogatory" : [],
        "summary" : {}
        }


def creating_bureaus():
    """ Creating the three Bureaus """
    transunion = Bureau()
    transunion.data['bureau'] = 'TransUnion'

    experian = Bureau()
    experian.data['bureau'] = 'Experian'

    equifax = Bureau()
    equifax.data['bureau'] = 'Equifax'

    return [transunion.data, experian.data, equifax.data]

def add_personal_data(bureau,data):
    """ Getting Personal Information """
    bureau['name'] = data['Name']
    bureau['also_known_as'] = data['alsoKnown']
    bureau['c_address'] = data['currentAddress']
    bureau['p_address'] = data['previousAddress']
    bureau['c_employer'] = data['employers']
    bureau['birth_year'] = data['dateOfBirth']
    bureau['credit_score'] = data['creditScore']

def add_summary(bureau,data):
    """ Getting Account Details """
    summary = {}
    summary['TotalAccounts'] = data['totalAccounts']
    summary['OpenAccounts'] = data['openAccounts']
    summary['CloseAccounts'] = data['closedAccounts']
    summary['DelinquentAccounts'] = data['delinquent']
    summary['DerogatoryAccounts'] = data['derogatory']
    summary['TotalBalances'] = data['balance']
    summary['TotalMonthlyPayments'] = data['payment']
    bureau['summary'] = summary


def add_inquiries(bureau, data):
    """ Getting Inquiries """
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
    """ Getting Public Record """
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


def get_pos_neg_acc(bureau, data,acc_detail,num_acc):
    """
    Get Positive/Negative Accounts.

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing two-year payments information.
        acc_detail: All Account details that has been extracted

    Returns:
        None
    """
    neg_flags = ["30", "60", "90", "120", "150", "180", "co", "rf", "pp", "vs"]

    if bureau['bureau'] == 'TransUnion':
        process_sublists(acc_detail, data['Transunion'][num_acc], neg_flags)
    else:
        process_sublists(acc_detail, data[bureau['bureau']][num_acc], neg_flags)

def process_sublists(acc_detail, sublist, neg_flags):
    """
    Process sublists to update positive and negative counters.

    Args:
        bureau (Bureau): The Bureau instance.
        sublists (list): List of sublists containing payment information.
        neg_flags (list): List of negative flags.

    Returns:
        None
    """
    if any(flag in sublist for flag in neg_flags):
        acc_detail['negative'] = True
        # Find the specific flag that caused the negative status
        negative_reason = next((flag for flag in neg_flags if flag in sublist), None)
        acc_detail['negative_reason'] = negative_reason
        # # You can break out of the loop if you only want to capture the first negative reason
        # break
    else:
        acc_detail['negative'] = False
        acc_detail['negative_reason'] = '-'
    # for sublist in sublists:
    #     if any(flag in sublist for flag in neg_flags):
    #         acc_detail['negative'] = True
    #     else:
    #         acc_detail['negative'] = False



def get_pay_history(bureau, data, acc_detail,num_acc):
    """
    Getting 2 Year Payment History

    Args:
        bureau (Bureau): The Bureau instance.
        data (dict): The data containing two-year payments information.
        acc_detail: All Account details that has been extracted

    Returns:
        None
    """
    if bureau['bureau'] == 'TransUnion':
        process_sublists_history(acc_detail,
                                 data['twoYearPayments']['Transunion'][num_acc],
                                 data['twoYearPaymentsMonths'][num_acc],
                                 data['twoYearPaymentsYears'][num_acc])
    else:
        process_sublists_history(acc_detail,
                                 data['twoYearPayments'][bureau['bureau']][num_acc],
                                 data['twoYearPaymentsMonths'][num_acc],
                                 data['twoYearPaymentsYears'][num_acc])

def process_sublists_history(acc_detail, data,month,year):
    """
    Process sublists to update account history.

    Args:
        acc_detail: All Account details that has been extracted
        data (dict): The data containing two-year payments information.

    Returns:
        None
    """
    acc_detail['pay_history'] = []
    for i,stat in enumerate(data):
        c_data = {"date": {"M": month[i], "Y":year[i]}, "status": stat}
        acc_detail['pay_history'].append(c_data)



def add_acc_history(bureau, data):
    """ Getting All Accounts """
    len_acc = len(data['accountIds'])
    for i in range(len_acc):
        acc_detail = {}
        acc_detail['account_number'] = data['accountIds'][i]
        acc_detail['account_type'] = data['accountTypes'][i]
        acc_detail['account_status'] = data['accountStatuses'][i]
        acc_detail['monthly_payment'] = data['monthlyPayments'][i]
        acc_detail['date_opened'] = data['dateOpened'][i]
        acc_detail['current_balance'] = data['balances'][i]
        acc_detail['no_of_months'] = data['noOfMonths'][i]
        acc_detail['past_due'] = data['pastDues'][i]
        acc_detail['pay_status'] = data['paymentStatuses'][i]
        acc_detail['date_reported'] = data['lastReported'][i]
        acc_detail['date_last_active'] = data['lastActive'][i]
        acc_detail['date_last_payment'] = data['lastPaymentDate'][i]
        acc_detail['account_name'] = data['bankNames'][i]
        acc_detail['bureau_code'] = data['bureauCodes'][i]
        if bureau['bureau'] == 'TransUnion':
            acc_detail['derogatory'] = data['derogatoryFlags']['Transunion'][i]
        else:
            acc_detail['derogatory'] = data['derogatoryFlags'][bureau['bureau']][i]

        get_pos_neg_acc(bureau,data['twoYearPayments'],acc_detail,num_acc=i)
        get_pay_history(bureau,data,acc_detail,num_acc=i)

        if acc_detail['account_name'] not in bureau['account_history']:
            bureau['account_history'][acc_detail['account_name']] = []
            bureau['account_history'][acc_detail['account_name']].append(acc_detail)
        else:
            bureau['account_history'][acc_detail['account_name']].append(acc_detail)




def report_data_idiq(data):
    """ Creating Report """
    repo_data = creating_bureaus() # transunion, experian, equifax
    bureaus_list = ['TransUnion', 'Experian', 'Equifax']

    # file = "D:/Codistan/codistan/CreditButterfly/scripts/ReportAnalysis/IdentityIQ/data.json"

    # with open(file, encoding="utf-8") as f:
    #     data = json.load(f)

    for i, bureau in enumerate(repo_data):
        add_personal_data(bureau, data[bureaus_list[i]])
        add_inquiries(bureau,data['inquiries'])
        add_pub_record(bureau,data['publicRecords'])
        add_summary(bureau,data[bureaus_list[i]])
        add_acc_history(bureau,data[bureaus_list[i]]['accountsInformation'])

    return repo_data
#     print(repo_data)

# report_data()
