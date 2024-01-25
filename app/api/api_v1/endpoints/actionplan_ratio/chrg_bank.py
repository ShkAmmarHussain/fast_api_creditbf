##################################################################################################################
##################################################################################################################
##################################################################################################################


import json

def derog_accnts(path_json):

    report = path_json
    # with open(path_json) as report:
    #     report = json.load(report)


    accnts = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['TradeLinePartition']
    
    
    try:
        pub_records = report['BundleComponents']['BundleComponent'][6]['TrueLinkCreditReportType']['PulblicRecordPartition']
    except:
        pub_records = ''
    

    Experian = {
                "bureau" : '',
                "negative" : 0,
                "derogatory" : []
            }

    equifax = {
                "bureau" : '',
                "negative" : 0,
                "derogatory" : []
            }

    transunion = {
                "bureau" : '',
                "negative" : 0,
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


    
    # tmp_negative = 0
    for acc in accnts:
        tmp_derog = {}
        
        if type(acc['Tradeline']) == type([]):
            acc['Tradeline'] = acc['Tradeline'][0]
        

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
        

        if acc['accountTypeSymbol'].lower() == ('y') or acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True:
            tmp_derog = {
                "accnt_nmbr" : acc['Tradeline']['accountNumber'],
                "issues" : []
            }
            # tmp_negative += 1
            
        if acc['accountTypeSymbol'].lower() == ('u' or 'y') and tmp_derog['accnt_nmbr']:
            tmp_derog['issues'].append("collection_account")
    
        if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' and tmp_derog['accnt_nmbr']:
            tmp_derog['issues'].append("chargeoff")
    
        if ttl_late > 0 and tmp_derog['accnt_nmbr']:
            tmp_derog['issues'].append(f"late_payments: {ttl_late}")
    
        if stat == True and tmp_derog['accnt_nmbr']:
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
            if len(tmp_derog) > 0:
                if len(tmp_derog['issues']) > 0:
                    if tmp_derog not in Experian['derogatory']:
                        Experian['derogatory'].append(tmp_derog)
            
            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                Experian['negative'] += 1
            
            Experian['bureau'] = bureau
            
            
            
            


        elif bureau.lower() == 'equifax':
            if len(tmp_derog) > 0:
                if len(tmp_derog['issues']) > 0:
                    if tmp_derog not in equifax['derogatory']:
                        equifax['derogatory'].append(tmp_derog)
            
            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                equifax['negative'] += 1
            
            equifax['bureau'] = bureau
            
        elif bureau.lower() == 'transunion':
            if len(tmp_derog) > 0:
                if len(tmp_derog['issues']) > 0:
                    if tmp_derog not in transunion['derogatory']:
                        transunion['derogatory'].append(tmp_derog)
            
            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                transunion['negative'] += 1
            
            transunion['bureau'] = bureau
            
    derog_accnt = {
        "Transunion": transunion,
        "Equifax": equifax,
        "Experian":Experian
    }

    return derog_accnt
    # print(tmp_negative)
    # print(equifax)




# path_json = "D:/Codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/WALTER KNAPP92.json"

# derog_accnt = derog_accnts(path_json)



def detail(path_json,bur):
    charge_off = {}
    backruptcy = {}

    derog_accnt = derog_accnts(path_json)
    for bureau,detail in derog_accnt.items():
        if bureau.lower() == bur.lower():
            for acc in detail['derogatory']:
                for issues in acc['issues']:
                    if 'chargeoff' in issues:
                        charge_off[acc['accnt_nmbr']] = 'chargeoff'
                    if 'bankruptcy' in issues:
                        backruptcy[acc['accnt_nmbr']] = 'bankruptcy'
                        # print(detail['derogatory'])
    chrg_bank = {
        'chargeoff' : charge_off,
        'bankruptcy': backruptcy
    }
    return chrg_bank

# detail(derog_accnt,'equifax')
