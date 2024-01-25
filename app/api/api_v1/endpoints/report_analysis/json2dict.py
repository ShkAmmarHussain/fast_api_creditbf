
import json
import os
from datetime import datetime

# path = os.getcwd().replace('\\','/')

# path_json = f"{path}/Credit_Reports/Credit_report_SmartCredit_json/AAS MUNDY1.json"

def json2dict(path_json):
    print("entered json")
    # with open(path_json) as report:
    #     report = json.load(report)
    report = path_json
    print("before acc")
    accnts = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['TradeLinePartition']
    print("before tns")
    trns_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['TransUnion']
    equif_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Equifax']
    exper_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Experian']
    print("before inq")
    inq_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['InquirySummary']
    pub_rec_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']

    creditscores = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Borrower']['CreditScore']

    print("before bureau")
    Experian = {
                "Bureau" : '',
                "Total Accounts" : 0,
                "Open Accounts" : 0,
                "Close Accounts" : 0,
                "Delinquent Accounts" : 0,
                "Derogatory Accounts" : 0,
                "Total Balances" : 0,
                "Total Monthly Payments" : 0,
                "Late 30 Count" : 0,
                "Late 60 Count" : 0,
                "Late 90 Count" : 0,
                "No of Revolving Acc" : 0,
                "No of Installment": 0,
                "No of Mortgage": 0,
                "No of Open Acc": 0,
                "No of Unknown Acc": 0,
                "No of Collection Acc": 0,
                "No of line of credit Acc": 0,
                "No of Inq": 0,
                "No of Public Record": 0,
                "Age of Oldest Account" : 0,
                "Open Student loans" : 0,
                "Credit Limit" : 0,
                "Credit Score" : 0
            }

    equifax = {
                "Bureau" : '',
                "Total Accounts" : 0,
                "Open Accounts" : 0,
                "Close Accounts" : 0,
                "Delinquent Accounts" : 0,
                "Derogatory Accounts" : 0,
                "Total Balances" : 0,
                "Total Monthly Payments" : 0,
                "Late 30 Count" : 0,
                "Late 60 Count" : 0,
                "Late 90 Count" : 0,
                "No of Revolving Acc" : 0,
                "No of Installment": 0,
                "No of Mortgage": 0,
                "No of Open Acc": 0,
                "No of Unknown Acc": 0,
                "No of Collection Acc": 0,
                "No of line of credit Acc": 0,
                "No of Inq": 0,
                "No of Public Record": 0,
                "Age of Oldest Account" : 0,
                "Open Student loans" : 0,
                "Credit Limit" : 0,
                "Credit Score" : 0
            }


    transunion = {
                "Bureau" : '',
                "Total Accounts" : 0,
                "Open Accounts" : 0,
                "Close Accounts" : 0,
                "Delinquent Accounts" : 0,
                "Derogatory Accounts" : 0,
                "Total Balances" : 0,
                "Total Monthly Payments" : 0,
                "Late 30 Count" : 0,
                "Late 60 Count" : 0,
                "Late 90 Count" : 0,
                "No of Revolving Acc" : 0,
                "No of Installment": 0,
                "No of Mortgage": 0,
                "No of Open Acc": 0,
                "No of Unknown Acc": 0,
                "No of Collection Acc": 0,
                "No of line of credit Acc": 0,
                "No of Inq": 0,
                "No of Public Record": 0,
                "Age of Oldest Account" : 0,
                "Open Student loans" : 0,
                "Credit Limit" : 0,
                "Credit Score" : 0
            }




    for creditscore in creditscores:
        if creditscore['Source']['Bureau']['description'].lower() == 'Experian':
            Experian['Credit Score'] = creditscore['riskScore']
        elif creditscore['Source']['Bureau']['description'].lower() == 'transunion':
            transunion['Credit Score'] = creditscore['riskScore']
        elif creditscore['Source']['Bureau']['description'].lower() == 'equifax':
            equifax['Credit Score'] = creditscore['riskScore']

    # print(accnts[0])
    ageinyears = 0
    # creditlimit = 0
    for acc in accnts:
        if type(acc['Tradeline']) == type([]):
            # print(acc['Tradeline'])
            acc['Tradeline'] = acc['Tradeline'][0]
        
        try:
            temp_age = datetime.strptime(acc['Tradeline']['dateReported'], "%Y-%m-%d") - datetime.strptime(acc['Tradeline']['dateOpened'], "%Y-%m-%d")
        except:
            temp_age = datetime.strptime(acc['Tradeline']['dateReported'], "%Y-%m-%d") - datetime.strptime(acc['Tradeline']['dateAccountStatus'], "%Y-%m-%d")
        temp_age = temp_age.days // 365
        if temp_age > ageinyears:
            ageinyears = temp_age

        print(ageinyears)

        try:
            bureau = acc['Tradeline']['bureau']
        except:
            # bureau = str(acc['Tradeline'][8]['bureau']["description"])
            bureau = str(acc['Tradeline'][8]['bureau'])



        if bureau.lower() == 'experian':
            print("experian")
            Experian['Age of Oldest Account'] = ageinyears
            Experian['Bureau'] = bureau
            Experian['Total Accounts'] = int(exper_acc_summary['TotalAccounts'])
            Experian['Open Accounts'] = int(exper_acc_summary['OpenAccounts'])
            Experian['Close Accounts'] = int(exper_acc_summary['CloseAccounts'])
            Experian['Delinquent Accounts'] = int(exper_acc_summary['DelinquentAccounts'])
            Experian['Derogatory Accounts'] = int(exper_acc_summary['DerogatoryAccounts'])
            Experian['Total Balances'] = int(exper_acc_summary['TotalBalances'])
            Experian['Total Monthly Payments'] = int(exper_acc_summary['TotalMonthlyPayments'])
            try:
                Experian['Late 30 Count'] += int(acc['Tradeline']['GrantedTrade']['late30Count'])
                Experian['Late 60 Count'] += int(acc['Tradeline']['GrantedTrade']['late60Count'])
                Experian['Late 90 Count'] += int(acc['Tradeline']['GrantedTrade']['late90Count'])
            except:
                pass
            Experian['No of Inq'] = int(inq_summary['Experian']['NumberInLast2Years'])
            Experian['No of Public Record'] = int(pub_rec_summary['Experian']['NumberOfRecords'])

            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except:
                pass

            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'r':
                Experian['No of Revolving Acc'] += 1
            elif acc_type.lower() == 'i':
                Experian['No of Installment'] +=1
            elif acc_type.lower() == 'm':
                Experian['No of Mortgage'] += 1
            elif acc_type.lower() == 'o':
                Experian['No of Open Acc'] += 1
            elif acc_type.lower() == 'u':
                Experian['No of Unknown Acc'] +=1
            elif acc_type.lower() == 'y':
                Experian['No of Collection Acc'] +=1
            elif acc_type.lower() == 'c':
                Experian['No of line of credit Acc'] +=1
            
            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
            #     Experian['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            try:
                Experian['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            except:
                pass

            if 'Remark' in acc['Tradeline']:
                # print(acc['Tradeline']['Remark']['RemarkCode']['description'] + '\n')
                if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                    list_of_studentloan = ['student loan','transferred','defaulted','collection']
                    for loan in list_of_studentloan:
                        try:
                            if loan in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                                Experian['Open Student loans'] +=1
                        except:
                            if loan in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                                Experian['Open Student loans'] +=1

            

            
        elif bureau.lower() == 'equifax':
            print("equifax")
            equifax['Age of Oldest Account'] = ageinyears
            equifax['Bureau'] = bureau
            equifax['Total Accounts'] = int(equif_acc_summary['TotalAccounts'])
            equifax['Open Accounts'] = int(equif_acc_summary['OpenAccounts'])
            equifax['Close Accounts'] = int(equif_acc_summary['CloseAccounts'])
            equifax['Delinquent Accounts'] = int(equif_acc_summary['DelinquentAccounts'])
            equifax['Derogatory Accounts'] = int(equif_acc_summary['DerogatoryAccounts'])
            equifax['Total Balances'] = int(equif_acc_summary['TotalBalances'])
            equifax['Total Monthly Payments'] = int(equif_acc_summary['TotalMonthlyPayments'])
            try:
                equifax['Late 30 Count'] += int(acc['Tradeline']['GrantedTrade']['late30Count'])
                equifax['Late 60 Count'] += int(acc['Tradeline']['GrantedTrade']['late60Count'])
                equifax['Late 90 Count'] += int(acc['Tradeline']['GrantedTrade']['late90Count'])
            except:
                pass
            equifax['No of Inq'] = int(inq_summary['Equifax']['NumberInLast2Years'])
            equifax['No of Public Record'] = int(pub_rec_summary['Equifax']['NumberOfRecords'])

            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except:
                pass

            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'r':
                equifax['No of Revolving Acc'] += 1
            elif acc_type.lower() == 'i':
                equifax['No of Installment'] +=1
            elif acc_type.lower() == 'm':
                equifax['No of Mortgage'] += 1
            elif acc_type.lower() == 'o':
                equifax['No of Open Acc'] += 1
            elif acc_type.lower() == 'u':
                equifax['No of Unknown Acc'] +=1
            elif acc_type.lower() == 'y':
                equifax['No of Collection Acc'] +=1
            elif acc_type.lower() == 'c':
                equifax['No of line of credit Acc'] +=1
            
            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
            #     equifax['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            try:
                equifax['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            except:
                pass

            if 'Remark' in acc['Tradeline']:
                # print(acc['Tradeline']['Remark'][0]['RemarkCode']['description'])
                if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                    list_of_studentloan = ['student loan','transferred','defaulted','collection']
                    for loan in list_of_studentloan:
                        try:
                            if loan in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                                equifax['Open Student loans'] +=1
                        except:
                            if loan in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                                equifax['Open Student loans'] +=1
                

            
        elif bureau.lower() == 'transunion':
            print("transunion")
            transunion['Age of Oldest Account'] = ageinyears
            transunion['Bureau'] = bureau
            transunion['Total Accounts'] = trns_acc_summary['TotalAccounts']
            transunion['Open Accounts'] = trns_acc_summary['OpenAccounts']
            transunion['Close Accounts'] = trns_acc_summary['CloseAccounts']
            transunion['Delinquent Accounts'] = trns_acc_summary['DelinquentAccounts']
            transunion['Derogatory Accounts'] = trns_acc_summary['DerogatoryAccounts']
            transunion['Total Balances'] = trns_acc_summary['TotalBalances']
            transunion['Total Monthly Payments'] = trns_acc_summary['TotalMonthlyPayments']
            try:
                transunion['Late 30 Count'] += int(acc['Tradeline']['GrantedTrade']['late30Count'])
                transunion['Late 60 Count'] += int(acc['Tradeline']['GrantedTrade']['late60Count'])
                transunion['Late 90 Count'] += int(acc['Tradeline']['GrantedTrade']['late90Count'])
            except:
                pass
            transunion['No of Inq'] = int(inq_summary['TransUnion']['NumberInLast2Years'])
            transunion['No of Public Record'] = int(pub_rec_summary['TransUnion']['NumberOfRecords'])

            print("here")
            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except:
                pass

            acc_type = acc['accountTypeSymbol']
            print(acc_type.lower())
            if acc_type.lower() == 'r':
                transunion['No of Revolving Acc'] += 1
            elif acc_type.lower() == 'i':
                transunion['No of Installment'] +=1
            elif acc_type.lower() == 'm':
                transunion['No of Mortgage'] += 1
            elif acc_type.lower() == 'o':
                transunion['No of Open Acc'] += 1
            elif acc_type.lower() == 'u':
                transunion['No of Unknown Acc'] +=1
            elif acc_type.lower() == 'y':
                transunion['No of Collection Acc'] +=1
            elif acc_type.lower() == 'c':
                transunion['No of line of credit Acc'] +=1

            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
            #     transunion['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            try:
                transunion['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            except:
                pass

            if 'Remark' in acc['Tradeline']:
                if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                    list_of_studentloan = ['student loan','transferred','defaulted','collection']
                    for loan in list_of_studentloan:
                        try:
                            if loan in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                                transunion['Open Student loans'] +=1
                        except:
                            if loan in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                                transunion['Open Student loans'] +=1
    print("left json")
    return transunion,equifax,Experian
    print(transunion)


# path_json = "D:/Codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/LINDA GRIMM52.json"

# json2dict(path_json)