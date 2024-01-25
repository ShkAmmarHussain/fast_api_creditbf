##################################################################################################################
##################################################################################################################
##################################################################################################################


import json
import os

def json2dict(path_json):

    # with open(path_json) as report:
    #     report = json.load(report)
    report = path_json

    accnts = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['TradeLinePartition']
    trns_acc_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['TransUnion']
    equif_acc_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Equifax']
    exper_acc_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Experian']
    inq_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['InquirySummary']
    pub_rec_summary = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']
    inquiries = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['InquiryPartition']
    bureau_ttl_late = 0
    
    try:
        pub_records = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['PulblicRecordPartition']
    except:
        pub_records = ''
    

    Experian = {
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

    equifax = {
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

    transunion = {
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
    
    
    if len(pub_records) > 1:
        for pub_record in pub_records:
            if "Bankruptcy" in pub_record['PublicRecord']:
                tmp_pubrec = {
                    'date_filed' : pub_record['PublicRecord']['dateFiled'],
                    'court_name': pub_record['PublicRecord']['courtName']
                }
                if pub_record['PublicRecord']['bureau'].lower() == 'equifax':
                    equifax['pub_record'].append(tmp_pubrec)
                elif pub_record['PublicRecord']['bureau'].lower() == 'experian':
                    Experian['pub_record'].append(tmp_pubrec)
                elif pub_record['PublicRecord']['bureau'].lower() == 'transunion':
                    transunion['pub_record'].append(tmp_pubrec)
    
    elif pub_records == 1:
        if "Bankruptcy" in pub_records['PublicRecord']:
            tmp_pubrec = {
                'date_filed' : pub_records['PublicRecord']['dateFiled'],
                'court_name': pub_records['PublicRecord']['courtName']
            }
            if pub_records['PublicRecord']['bureau'].lower() == 'equifax':
                equifax['pub_record'].append(tmp_pubrec)
            elif pub_records['PublicRecord']['bureau'].lower() == 'experian':
                Experian['pub_record'].append(tmp_pubrec)
            elif pub_records['PublicRecord']['bureau'].lower() == 'transunion':
                transunion['pub_record'].append(tmp_pubrec)


    for inquiry in inquiries:
        tmp_inq = {
            "inquirydate" : inquiry['Inquiry']['inquiryDate'],
            "account_name" : inquiry['Inquiry']['subscriberName'],
        }
        if inquiry['Inquiry']['bureau'].lower() == 'equifax':
            equifax['inquiry'].append(tmp_inq)
        elif inquiry['Inquiry']['bureau'].lower() == 'experian':
            Experian['inquiry'].append(tmp_inq)
        elif inquiry['Inquiry']['bureau'].lower() == 'transunion':
            transunion['inquiry'].append(tmp_inq)
    
    
    for acc in accnts:
        tmp_derog = {}
        if type(acc['Tradeline']) == type([]):
            acc['Tradeline'] = acc['Tradeline'][-1]
        

        stat = False
        if "Remark" in acc['Tradeline']:
            try:
                if "bankruptcy" in acc['Tradeline']['Remark']['RemarkCode']['description']:
                    stat = True
            except:
                if "bankruptcy" in acc['Tradeline']['Remark'][0]['RemarkCode']['description']:
                    stat = True
    
        try:
            late = acc['Tradeline']['GrantedTrade']
            ttl_late = int(late['late90Count']) + int(late['late60Count']) + int(late['late30Count'])
        except:
            ttl_late = 0


        if acc['accountTypeSymbol'].lower() == 'u' or acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True:
            tmp_derog = {
                "accnt_name" : acc['Tradeline']['creditorName'],
                "issues" : []
            }
            tmp_derog['issues'].append("collection_account")
    
        if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff':
            tmp_derog['issues'].append("status_charge_off")
    
        if ttl_late > 0:
            tmp_derog['issues'].append(f"late_payments: {ttl_late}")
    
        if stat == True:
            tmp_derog['issues'].append("Bankruptcy")


        debt = False
        if "Remark" in acc['Tradeline']:
            try:
                if "debt" in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                    debt = True
            except:
                if "debt" in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                    debt = True


        try:
            bureau = acc['Tradeline']['bureau']
        except:
            bureau = str(acc['Tradeline'][8]['Bureau']["description"])

        if bureau.lower() == 'experian':
            
            Experian['late_pay'] += ttl_late

            if len(tmp_derog) > 0:
                if tmp_derog not in Experian['derogatory']:
                    Experian['derogatory'].append(tmp_derog)
            
            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                Experian['negative'] += 1
            
            Experian['positive'] = int(exper_acc_summary['TotalAccounts']) - Experian['negative']
            Experian['bureau'] = bureau
            Experian['total_accounts'] = int(exper_acc_summary['TotalAccounts'])
            Experian['delinquent_accounts'] = int(exper_acc_summary['DelinquentAccounts'])
            Experian['derogatory_accounts'] = int(exper_acc_summary['DerogatoryAccounts'])
            try:
                Experian['no_of_inq'] = int(inq_summary['Experian']['NumberInLast2Years'])
                Experian['no_of_pub_record'] = int(pub_rec_summary['Experian']['NumberOfRecords'])
            except Exception as e:
                pass

            if report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                Experian['credit_score'] = int(report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                Experian['credit_score'] = int(report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                Experian['credit_score'] = int(report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['riskScore'])

            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'y':
                Experian['no_of_collection'] +=1
            
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['accountTypeSymbol'].lower() == 'r':
                Experian['revolving_credit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['Tradeline']['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
                Experian['credit_card_balance'] += int(acc['Tradeline']['currentBalance'])
            


        elif bureau.lower() == 'equifax':

            equifax['late_pay'] += ttl_late

            if len(tmp_derog) > 0:
                if tmp_derog not in equifax['derogatory']:
                    equifax['derogatory'].append(tmp_derog)
            
            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                equifax['negative'] += 1
            
            equifax['positive'] = int(equif_acc_summary['TotalAccounts']) - equifax['negative']
            equifax['bureau'] = bureau
            equifax['total_accounts'] = int(equif_acc_summary['TotalAccounts'])
            equifax['delinquent_accounts'] = int(equif_acc_summary['DelinquentAccounts'])
            equifax['derogatory_accounts'] = int(equif_acc_summary['DerogatoryAccounts'])
    
            try:
                equifax['no_of_inq'] = int(inq_summary['Equifax']['NumberInLast2Years'])
                
            except:
                pass
            equifax['no_of_pub_record'] = int(pub_rec_summary['Equifax']['NumberOfRecords'])

            if report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                equifax['credit_score'] = int(report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                equifax['credit_score'] = int(report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                equifax['credit_score'] = int(report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['riskScore'])

            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'y':
                equifax['no_of_collection'] +=1

            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['accountTypeSymbol'].lower() == 'r':
                equifax['revolving_credit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['Tradeline']['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
                equifax['credit_card_balance'] += int(acc['Tradeline']['currentBalance'])
                


        elif bureau.lower() == 'transunion':

            transunion['late_pay'] += ttl_late

            if len(tmp_derog) > 0:
                if tmp_derog not in transunion['derogatory']:
                    transunion['derogatory'].append(tmp_derog)
            
            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                transunion['negative'] += 1
            
            transunion['positive'] = int(trns_acc_summary['TotalAccounts']) - transunion['negative']
            transunion['bureau'] = bureau
            transunion['total_accounts'] = trns_acc_summary['TotalAccounts']
            transunion['delinquent_accounts'] = trns_acc_summary['DelinquentAccounts']
            transunion['derogatory_accounts'] = trns_acc_summary['DerogatoryAccounts']
            try:
                transunion['no_of_inq'] = int(inq_summary['TransUnion']['NumberInLast2Years'])
                transunion['no_of_pub_record'] = int(pub_rec_summary['TransUnion']['NumberOfRecords'])
            except Exception as e:
                pass


            if report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                transunion['credit_score'] = int(report['BundleComponents']['BundleComponent'][3]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                transunion['credit_score'] = int(report['BundleComponents']['BundleComponent'][4]['CreditScoreType']['riskScore'])
            if report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                transunion['credit_score'] = int(report['BundleComponents']['BundleComponent'][5]['CreditScoreType']['riskScore'])
        
            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'y':
                transunion['no_of_collection'] +=1
            
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['accountTypeSymbol'].lower() == 'r':
                transunion['revolving_credit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['Tradeline']['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
                transunion['credit_card_balance'] += int(acc['Tradeline']['currentBalance'])

    return transunion,equifax,Experian
    print(equifax)




# path_json = "D:/Codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/WALTER KNAPP92.json"

# json2dict(path_json)