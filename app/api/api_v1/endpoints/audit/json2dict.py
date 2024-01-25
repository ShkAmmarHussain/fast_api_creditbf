import json
import os

# path = os.getcwd().replace('\\','/')

# path_json = f"{path}/Credit_Reports/Credit_report_SmartCredit_json/AAS MUNDY1.json"

def json2dict(path_json):

    with open(path_json) as report:
        report = json.load(report)


    accnts = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['TradeLinePartition']
    trns_acc_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['TransUnion']
    equif_acc_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Equifax']
    exper_acc_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Experian']
    inq_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['InquirySummary']
    pub_rec_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']

    creditscores = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Borrower']['CreditScore']
    

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
                "No of Inq": 0,
                "No of Public Record": 0,
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
                "No of Inq": 0,
                "No of Public Record": 0,
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
                "No of Inq": 0,
                "No of Public Record": 0,
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
    n=0
    for acc in accnts:
        # print(type(acc['Tradeline']))
        if type(acc['Tradeline']) == type([]):
            # print(acc['Tradeline'])
            acc['Tradeline'] = acc['Tradeline'][0]
            
        # n+=1
        # print(n)
        try:
            bureau = acc['Tradeline']['bureau']
            # print(acc['Tradeline']['bureau'])
        except:
            bureau = str(acc['Tradeline'][8]['Bureau']["description"])
            # print(bureau)

        if bureau.lower() == 'experian':
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
                Experian['No of Inq'] = int(inq_summary['Experian']['NumberInLast2Years'])
                Experian['No of Public Record'] = int(pub_rec_summary['Experian']['NumberOfRecords'])
            except Exception as e:
                print("error in Experian is:\n",e)
                print("\n\n"+str(Experian['Late 30 Count']))
                pass

            if report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['riskScore'])

            acc_type = acc['accountTypeAbbreviation']
            if acc_type.lower() == 'revolving':
                Experian['No of Revolving Acc'] += 1
            elif acc_type.lower() == 'installment':
                Experian['No of Installment'] +=1
            elif acc_type.lower() == 'mortgage':
                Experian['No of Mortgage'] += 1
            elif acc_type.lower() == 'open account':
                Experian['No of Open Acc'] += 1
            elif acc_type.lower() == 'unknown':
                Experian['No of Unknown Acc'] +=1
            


        elif bureau.lower() == 'equifax':
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
                equifax['No of Inq'] = int(inq_summary['Equifax']['NumberInLast2Years'])
                
            except:
                pass
            equifax['No of Public Record'] = int(pub_rec_summary['Equifax']['NumberOfRecords'])

            if report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['riskScore'])

            acc_type = acc['accountTypeAbbreviation']
            if acc_type.lower() == 'revolving':
                equifax['No of Revolving Acc'] += 1
            elif acc_type.lower() == 'installment':
                equifax['No of Installment'] +=1
            elif acc_type.lower() == 'mortgage':
                equifax['No of Mortgage'] += 1
            elif acc_type.lower() == 'open account':
                equifax['No of Open Acc'] += 1
            elif acc_type.lower() == 'unknown':
                equifax['No of Unknown Acc'] +=1
                


        elif bureau.lower() == 'transunion':
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
                transunion['No of Inq'] = int(inq_summary['TransUnion']['NumberInLast2Years'])
                transunion['No of Public Record'] = int(pub_rec_summary['TransUnion']['NumberOfRecords'])
            except Exception as e:
                print("Trans error:\n"+e+"\n\n",acc)
                pass


            if report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['riskScore'])
        
            acc_type = acc['accountTypeAbbreviation']
            if acc_type.lower() == 'revolving':
                transunion['No of Revolving Acc'] += 1
            elif acc_type.lower() == 'installment':
                transunion['No of Installment'] +=1
            elif acc_type.lower() == 'mortgage':
                transunion['No of Mortgage'] += 1
            elif acc_type.lower() == 'open account':
                transunion['No of Open Acc'] += 1
            elif acc_type.lower() == 'unknown':
                transunion['No of Unknown Acc'] +=1

    return transunion,equifax,Experian
    print(equifax)

