import json

def json2dict(path_json):
    with open(path_json) as report_file:
        report = json.load(report_file)

    bureau_data = {
        "experian": initialize_bureau_data(),
        "equifax": initialize_bureau_data(),
        "transunion": initialize_bureau_data(),
    }

    process_public_records(report, bureau_data)
    process_inquiries(report, bureau_data)
    process_accounts(report, bureau_data)

    return bureau_data

def initialize_bureau_data():
    return {
        "bureau": "",
        "total_accounts": 0,
        "delinquent_accounts": 0,
        "derogatory_accounts": 0,
        "no_of_collection": 0,
        "no_of_inq": 0,
        "no_of_pub_record": 0,
        "credit_score": 0,
        "positive": 0,
        "negative": 0,
        "revolving_credit": 0,
        "credit_card_balance": 0,
        "inquiry": [],
        "pub_record": [],
        "derogatory": [],
    }

def process_public_records(report, bureau_data):
    try:
        public_records = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['PulblicRecordPartition']
    except KeyError:
        public_records = []

    for pub_record in public_records:
        if "Bankruptcy" in pub_record:
            tmp_pubrec = {
                'date_filed': pub_record['PublicRecord']['dateFiled'],
                'court_name': pub_record['PublicRecord']['courtName']
            }
            bureau = pub_record['PublicRecord']['bureau'].lower()
            bureau_data[bureau]['pub_record'].append(tmp_pubrec)

def process_inquiries(report, bureau_data):
    inquiries = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['InquiryPartition']
    
    for inquiry in inquiries:
        tmp_inq = {
            "inquirydate": inquiry['Inquiry']['inquiryDate'],
            "account_name": inquiry['Inquiry']['subscriberName'],
        }
        bureau = inquiry['Inquiry']['bureau'].lower()
        bureau_data[bureau]['inquiry'].append(tmp_inq)

def process_accounts(report, bureau_data):
    accnts = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['TradeLinePartition']
    summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']
    for acc in accnts:
        if isinstance(acc['Tradeline'], list):
            acc['Tradeline'] = acc['Tradeline'][0]

        bureau = get_bureau(acc['Tradeline'])
        tmp_derog = initialize_derogatory_data()
        late_count = get_late_count(acc['Tradeline'])
        is_bankruptcy = check_bankruptcy(acc['Tradeline'])
        is_debt = check_debt(acc['Tradeline'])

        if is_bankruptcy or is_debt or late_count > 0:
            tmp_derog["accnt_name"] = acc['Tradeline']['creditorName']
            tmp_derog["issues"] = []

        if acc['accountTypeSymbol'].lower() == 'y':
            bureau_data[bureau]['no_of_collection'] += 1

        if is_bankruptcy:
            tmp_derog['issues'].append("Bankruptcy")

        if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff':
            tmp_derog['issues'].append("status_charge_off")

        if late_count > 0:
            tmp_derog['issues'].append(f"late_payments: {late_count}")

        if is_debt:
            tmp_derog['issues'].append("collection_account")

        if bureau.lower() == 'experian':
            bureau_data[bureau]['derogatory'].append(tmp_derog)
            bureau_data[bureau]['negative'] += 1

        key = []
        if bureau.lower() == 

        bureau_data[bureau]['positive'] = bureau_data[bureau]['total_accounts'] - bureau_data[bureau]['negative']
        bureau_data[bureau]['bureau'] = bureau
        bureau_data[bureau]['total_accounts'] = get_total_accounts(summary['TradelineSummary'][bureau])
        bureau_data[bureau]['delinquent_accounts'] = get_delinquent_accounts(summary['TradelineSummary'][bureau])
        bureau_data[bureau]['derogatory_accounts'] = get_derogatory_accounts(summary['TradelineSummary'][bureau])
        bureau_data[bureau]['no_of_inq'] = get_inquiry_count(report, bureau)
        bureau_data[bureau]['no_of_pub_record'] = get_public_record_count(report, bureau)
        bureau_data[bureau]['credit_score'] = get_credit_score(report, bureau)
        bureau_data[bureau]['revolving_credit'] += get_revolving_credit(acc)
        bureau_data[bureau]['credit_card_balance'] += get_credit_card_balance(acc)

def get_bureau(tradeline):
    try:
        # bureau = tradeline['bureau'].lower()
        bureau = tradeline['bureau']
    except KeyError:
        bureau = str(tradeline[8]['Bureau']["description"])
    return bureau

def initialize_derogatory_data():
    return {
        "accnt_name": "",
        "issues": []
    }

def get_late_count(tradeline):
    try:
        late = tradeline['GrantedTrade']
        return int(late['late90Count']) + int(late['late60Count']) + int(late['late30Count'])
    except KeyError:
        return 0

def check_bankruptcy(tradeline):
    try:
        return "bankruptcy" in tradeline['Remark']['RemarkCode']['description'].lower()
    except KeyError:
        return False

def check_debt(tradeline):
    try:
        return "debt" in tradeline['Remark']['RemarkCode']['description'].lower()
    except KeyError:
        return False

def get_total_accounts(tradeline):
    return int(tradeline['TotalAccounts'])

def get_delinquent_accounts(tradeline):
    return int(tradeline['DelinquentAccounts'])

def get_derogatory_accounts(tradeline):
    return int(tradeline['DerogatoryAccounts'])

def get_inquiry_count(report, bureau):
    try:
        return int(report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['InquirySummary'][bureau.capitalize()]['NumberInLast2Years'])
    except KeyError:
        return 0

def get_public_record_count(report, bureau):
    try:
        return int(report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary'][bureau.capitalize()]['NumberOfRecords'])
    except KeyError:
        return 0

def get_credit_score(report, bureau):
    for i in range(3, 6):
        try:
            source = report['BundleComponents']['BundleComponent'][i]['CreditScoreType']['Source']['Bureau']['description'].lower()
            if source == bureau:
                return int(report['BundleComponents']['BundleComponent'][i]['CreditScoreType']['riskScore'])
        except KeyError:
            pass
    return 0

def get_revolving_credit(tradeline):
    if tradeline['OpenClosed']['symbol'].lower() == 'o' and tradeline['accountTypeSymbol'].lower() == 'r':
        return int(tradeline['GrantedTrade']['CreditLimit'])
    return 0

def get_credit_card_balance(tradeline):
    if tradeline['OpenClosed']['symbol'].lower() == 'o' and tradeline['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
        return int(tradeline['currentBalance'])
    return 0

path_json = "D:/Codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/WALTER KNAPP92.json"
print(json2dict(path_json))
