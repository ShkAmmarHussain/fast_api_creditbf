""" Getting Utilization Ratio Data """
import dataclasses

@dataclasses.dataclass
class Suggestion:
    """ Creating bureaus """
    def __init__(self) -> None:
        self.data = {
            "limit" : "-",
            "acc_nmbr" : "-",
            "balance" : "-",
            "bnk_name" : "-",
            # "bureau" : "-"
        }

def create_suggestion():
    """Empty Suggestion"""
    return Suggestion().data


def smartcredit_ratio(report):
    """ Getting Utilization ratio data from smart credit """
    accnts = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['TradeLinePartition']

    tmp = []
    for acc in accnts:
        acc_type = acc['accountTypeSymbol']
        
        if type(acc['Tradeline']) == type([]):
            acc['Tradeline'] = acc['Tradeline'][-1]
        acc_status = acc['Tradeline']['OpenClosed']['symbol']
        if acc_type.lower() == 'r' and acc_status.lower() == 'o':
            tmp_data = create_suggestion()
            tmp_data['limit'] = acc['Tradeline']['GrantedTrade']['CreditLimit']
            tmp_data['acc_nmbr'] = acc['Tradeline']['accountNumber']
            tmp_data['balance'] = acc['Tradeline']['currentBalance']
            tmp_data['bnk_name'] = acc['Tradeline']['creditorName']
            tmp.append(tmp_data)
    print(tmp)
    return tmp


def idiq_ratio(report):
    """ Getting Utilization ratio data from idiq """
    bureaus = ['TransUnion', 'Experian', 'Equifax']
    tmp = []
    for bureau in bureaus:
        acc_len = len(report[bureau]['accountsInformation']['accountTypes'])
        informations = report[bureau]['accountsInformation']
        for i in range(acc_len):
            if informations['accountTypes'][i].lower() == 'revolving' and informations['accountStatuses'][i].lower() == 'open':
                tmp_data = create_suggestion()
                tmp_data['limit'] = informations['creditLimits'][i]
                tmp_data['acc_nmbr'] = informations['accountIds'][i]
                tmp_data['balance'] = informations['balances'][i]
                tmp_data['bnk_name'] = informations['bankNames'][i]
                tmp.append(tmp_data)

    return tmp


def ratio_data(path_json, provider):
    """ Utilization Ratio """
    report = path_json

    if provider == "smartcredit":
        return smartcredit_ratio(report)
    if provider == "idiq":
        return idiq_ratio(report)
