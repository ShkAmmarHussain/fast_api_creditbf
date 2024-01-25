import json


def report_data(path_json):
    print("entered report")
    # with open(path_json) as report:
    #     report = json.load(report)
    
    # print("entered 4 report data")
    report = path_json


    accnts = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['TradeLinePartition']
    trns_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['TransUnion']
    trns_inq_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['InquirySummary']['TransUnion']
    trns_pub_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']['TransUnion']

    equif_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Equifax']
    equif_inq_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['InquirySummary']['Equifax']
    equif_pub_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']['Equifax']

    exper_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Experian']
    exper_inq_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['InquirySummary']['Experian']
    exper_pub_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']['Experian']

    # inq_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['InquirySummary']
    # pub_rec_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['PublicRecordSummary']
    inquiries = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['InquiryPartition']
    borrower = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Borrower']

    trns_acc_summary['no_of_collection'] = 0
    equif_acc_summary['no_of_collection'] = 0
    exper_acc_summary['no_of_collection'] = 0

    trns_summary = {
        "account_summary" : trns_acc_summary,
        "inquiry_summary" : trns_inq_summary,
        "pub_rec_summary" : trns_pub_summary
    }

    equif_summary = {
        "account_summary" : equif_acc_summary,
        "inquiry_summary" : equif_inq_summary,
        "pub_rec_summary" : equif_pub_summary
    }

    exper_summary = {
        "account_summary" : exper_acc_summary,
        "inquiry_summary" : exper_inq_summary,
        "pub_rec_summary" : exper_pub_summary
    }

    try:
        pub_records = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['PulblicRecordPartition']
    except:
        pub_records = ''


    Experian = {
                "bureau" : '',
                "name" : '',
                "address" : '',
                "c_employer" : '',
                "p_employer" : '',
                "birth_year" : '-',
                # "total_accounts" : 0,
                # "delinquent_accounts" : 0,
                # "derogatory_accounts" : 0,
                # "no_of_collection" : 0, # No. of Unknowns
                # "no_of_inq": 0,
                # "no_of_pub_record": 0,
                "credit_score" : 0,
                "positive" : 0,
                "negative" : 0,
                # "revolving_credit" : 0,
                # "credit_card_balance" : 0,
                "account_history" : {},
                "inquiry" : [],
                "pub_record" : [],
                "derogatory" : [],
                "summary" : exper_summary
            }

    equifax = {
                "bureau" : '',
                "name" : '',
                "address" : '',
                "c_employer" : '',
                "p_employer" : '',
                "birth_year" : '-',
                # "total_accounts" : 0,
                # "delinquent_accounts" : 0,
                # "derogatory_accounts" : 0,
                # "no_of_collection" : 0, # No. of Unknowns
                # "no_of_inq": 0,
                # "no_of_pub_record": 0,
                "credit_score" : 0,
                "positive" : 0,
                "negative" : 0,
                # "revolving_credit" : 0,
                # "credit_card_balance" : 0,
                "account_history" : {},
                "inquiry" : [],
                "pub_record" : [],
                "derogatory" : [],
                "summary" : equif_summary
            }

    transunion = {
                "bureau" : '',
                "name" : '',
                "address" : '',
                "c_employer" : '',
                "p_employer" : '',
                "birth_year" : '-',
                # "total_accounts" : 0,
                # "delinquent_accounts" : 0,
                # "derogatory_accounts" : 0,
                # "no_of_collection" : 0, # No. of Unknowns
                # "no_of_inq": 0,
                # "no_of_pub_record": 0,
                "credit_score" : 0,
                "positive" : 0,
                "negative" : 0,
                # "revolving_credit" : 0,
                # "credit_card_balance" : 0,
                "account_history" : {},
                "inquiry" : [],
                "pub_record" : [],
                "derogatory" : [],
                "summary" : trns_summary
            }

    def pub_rec(pub_record):
        if "Bankruptcy" in pub_record['PublicRecord']:
                tmp_pubrec = {
                    'type' : pub_record['PublicRecord']['Type']['abbreviation'],
                    'status' : pub_record['PublicRecord']['Status']['abbreviation'],
                    'date_filed' : pub_record['PublicRecord']['dateFiled'],
                    'reference_number' : pub_record['PublicRecord']['referenceNumber'],
                    'asset_amount' : pub_record['PublicRecord']['Bankruptcy']['assetAmount'],
                    'liability_amount' : pub_record['PublicRecord']['Bankruptcy']['liabilityAmount'],
                    'exempt_amount' : pub_record['PublicRecord']['Bankruptcy']['exemptAmount'],
                    'court_name': pub_record['PublicRecord']['courtName'],
                }
                if pub_record['PublicRecord']['bureau'].lower() == 'equifax':
                    equifax['pub_record'].append(tmp_pubrec)
                elif pub_record['PublicRecord']['bureau'].lower() == 'experian':
                    Experian['pub_record'].append(tmp_pubrec)
                elif pub_record['PublicRecord']['bureau'].lower() == 'transunion':
                    transunion['pub_record'].append(tmp_pubrec)
                # print(tmp_pubrec)


    # print(len(pub_records))
    if len(pub_records) > 1:
        for pub_record in pub_records:
            pub_rec(pub_record)
    elif len(pub_records) == 1:
        pub_rec(pub_records)

    def nega_reason(acc,late,stat,debt):
        neg_reason = []
        if acc == 'collection/chargeoff':
            neg_reason.append(acc)
        if late > 0:
            neg_reason.append(late)
        if stat is True:
            neg_reason.append("bankruptcy")
        if debt is True:
            neg_reason.append("unpaid_debt")
        return neg_reason

    print("before inquiry")
    for inquiry in inquiries:
        tmp_inq = {
            "inquirydate" : inquiry['Inquiry']['inquiryDate'],
            "subscriber_name" : inquiry['Inquiry']['subscriberName'],
            "business_type" : inquiry['Inquiry']['IndustryCode']['abbreviation']
        }
        if inquiry['Inquiry']['bureau'].lower() == 'equifax':
            equifax['inquiry'].append(tmp_inq)
        elif inquiry['Inquiry']['bureau'].lower() == 'experian':
            Experian['inquiry'].append(tmp_inq)
        elif inquiry['Inquiry']['bureau'].lower() == 'transunion':
            transunion['inquiry'].append(tmp_inq)

    names = borrower['BorrowerName']

    print("before name")
    for name in names:
        if name['Source']['Bureau']['symbol'].lower() == 'tuc':
            transunion['name'] = f"{name['Name']['first']} {name['Name']['middle']} {name['Name']['last']}"
        elif name['Source']['Bureau']['symbol'].lower() == 'exp':
            Experian['name'] = f"{name['Name']['first']} {name['Name']['middle']} {name['Name']['last']}"
        elif name['Source']['Bureau']['symbol'].lower() == 'eqf':
            equifax['name'] = f"{name['Name']['first']} {name['Name']['middle']} {name['Name']['last']}"

    addresses = borrower['BorrowerAddress']

    print("before address")
    for address in addresses:
        try:
            add = f"{address['CreditAddress']['houseNumber']} {address['CreditAddress']['streetName']} {address['CreditAddress']['city']} {address['CreditAddress']['stateCode']} {address['CreditAddress']['postalCode']}"
        except:
            add = f"{address['CreditAddress']['unparsedStreet']} {address['CreditAddress']['city']} {address['CreditAddress']['stateCode']} {address['CreditAddress']['postalCode']}"
        if address['Source']['Bureau']['symbol'].lower() == 'tuc':
            transunion['address'] = add
        elif address['Source']['Bureau']['symbol'].lower() == 'exp':
            Experian['address'] = add
        elif address['Source']['Bureau']['symbol'].lower() == 'eqf':
            equifax['address'] = add

    print("current employee")

    try:
        c_employer = borrower['Employer'][0]['name']
        print(c_employer)
        p_employer = borrower['Employer'][1]['name']
        print(p_employer)

        print("entered json")
        transunion['c_employer'], transunion['p_employer'] = c_employer , p_employer
        Experian['c_employer'], Experian['p_employer'] = c_employer , p_employer
        equifax['c_employer'], equifax['p_employer'] = c_employer , p_employer
    except:
        pass

    birth_year = borrower['Birth']


    print("before birth year")
    if isinstance(birth_year, list):
        for year in birth_year:
            tmp = year['BirthDate']['year']
            if year['Source']['Bureau']['symbol'].lower() == 'tuc':
                transunion['birth_year'] = tmp
            elif year['Source']['Bureau']['symbol'].lower() == 'exp':
                Experian['birth_year'] = tmp
            elif year['Source']['Bureau']['symbol'].lower() == 'eqf':
                equifax['birth_year'] = tmp
    else:
        tmp = birth_year['BirthDate']['year']
        if birth_year['Source']['Bureau']['symbol'].lower() == 'tuc':
            transunion['birth_year'] = tmp
        elif birth_year['Source']['Bureau']['symbol'].lower() == 'exp':
            Experian['birth_year'] = tmp
        elif birth_year['Source']['Bureau']['symbol'].lower() == 'eqf':
            equifax['birth_year'] = tmp
    print("before acc")
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

        print("before derog")
        if acc['Tradeline']['AccountCondition']['abbreviation'].lower() == 'derog':
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

            if stat is True:
                tmp_derog['issues'].append("Bankruptcy")

        print("before remark")
        debt = False
        if "Remark" in acc['Tradeline']:
            try:
                if "debt" in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                    debt = True
            except:
                if "debt" in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                    debt = True


        print("before acc_detail")
        acc_detail = {}
        try:
            acc_detail['account_number'] = acc['Tradeline']['accountNumber']
            acc_detail['account_type'] = acc['accountTypeDescription']
            acc_detail['account_status'] = acc['Tradeline']['OpenClosed']['abbreviation']
            try:
                acc_detail['monthly_payment'] = acc['Tradeline']['GrantedTrade']['monthlyPayment']
            except:
                acc_detail['monthly_payment'] = "-"
            acc_detail['date_opened'] = acc['Tradeline']['dateOpened']
            acc_detail['current_balance'] = acc['Tradeline']['currentBalance']
            try:
                acc_detail['no_of_months'] = acc['Tradeline']['GrantedTrade']['termMonths']
            except:
                acc_detail['no_of_months'] = '-'
            try:
                acc_detail['past_due'] = acc['Tradeline']['GrantedTrade']['amountPastDue']
            except:
                acc_detail['past_due'] = '-'
            acc_detail['pay_status'] = acc['Tradeline']['PayStatus']['description']
            acc_detail['date_reported'] =  acc['Tradeline']['dateReported']
            try:
                acc_detail['date_last_active'] =  acc['Tradeline']['dateClosed']
            except:
                acc_detail['date_last_active'] = '-'
            try:
                acc_detail['date_last_payment'] = acc['Tradeline']['GrantedTrade']['dateLastPayment']
            except:
                acc_detail['date_last_payment'] = '-'
            acc_detail['account_name'] = acc['Tradeline']['creditorName']
            acc_detail['bureau_code'] = acc['Tradeline']['AccountDesignator']['description']
            try:
                if "PayStatusHistory" in acc['Tradeline']['GrantedTrade']:
                    acc_detail['pay_history'] = acc['Tradeline']['GrantedTrade']['PayStatusHistory']['MonthlyPayStatus']
                else:
                    acc_detail['pay_history'] = ""
            except:
                acc_detail['pay_history'] = ""
        except Exception as e:
            print(e)
        # print('passed acc_detail')
        # acc_detail['account_number'] = acc['Tradeline']['accountNumber']
        # acc_detail['account_type'] = acc['accountTypeDescription']
        # # acc_detail['account_status'] = acc['Tradeline']['PayStatus']['description']
        # if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
        #     acc_detail['Negative'] = True
        # else:
        #     acc_detail['Negative'] = False



        try:
            bureau = acc['Tradeline']['bureau']
        except:
            bureau = str(acc['Tradeline'][8]['Bureau']["description"])

        if bureau.lower() == 'experian':

            # Experian['account_history'].append(acc_detail)

            if len(tmp_derog) > 0:
                if tmp_derog not in Experian['derogatory']:
                    Experian['derogatory'].append(tmp_derog)

            acc_detail['negative'] = False
            try:
                if acc['Tradeline']['DisputeFlag']['symbol'] == "F":
                    acc_detail['disputed'] = False
                else:
                    acc_detail['disputed'] = True
            except KeyError:
                acc_detail['disputed'] = False

            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat is True or debt is True:
                neg_reason = nega_reason(acc['Tradeline']['PayStatus']['description'].lower(),ttl_late,stat,debt)
                Experian['negative'] += 1
                acc_detail['negative'] = True
                acc_detail['negative_reason'] = neg_reason

            # if len(Experian['account_history']) != 0:
            if acc_detail['account_name'] not in Experian['account_history'].keys():
                # print(Experian['account_history'][acc_detail['account_name']])
                Experian['account_history'][acc_detail['account_name']] = []
                Experian['account_history'][acc_detail['account_name']].append(acc_detail)
                # equifax['account_history'].append(acc_detail)
            else:
                # print("at else")
                Experian['account_history'][acc_detail['account_name']].append(acc_detail)


            Experian['positive'] = int(exper_acc_summary['TotalAccounts']) - Experian['negative']
            Experian['bureau'] = bureau
            # Experian['total_accounts'] = int(exper_acc_summary['TotalAccounts'])
            # Experian['delinquent_accounts'] = int(exper_acc_summary['DelinquentAccounts'])
            # Experian['derogatory_accounts'] = int(exper_acc_summary['DerogatoryAccounts'])
            # try:
            #     Experian['no_of_inq'] = int(inq_summary['Experian']['NumberInLast2Years'])
            #     Experian['no_of_pub_record'] = int(pub_rec_summary['Experian']['NumberOfRecords'])
            # except Exception as e:
            #     pass
            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['credit_score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['credit_score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['credit_score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except:
                pass
            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'y':
                Experian['summary']['account_summary']['no_of_collection'] +=1
                print(f"col: {Experian['summary']['account_summary']['no_of_collection']}")
            
            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['accountTypeSymbol'].lower() == 'r':
            #     Experian['revolving_credit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])

            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['Tradeline']['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
            #     Experian['credit_card_balance'] += int(acc['Tradeline']['currentBalance'])



        elif bureau.lower() == 'equifax':

            if len(tmp_derog) > 0:
                if tmp_derog not in equifax['derogatory']:
                    equifax['derogatory'].append(tmp_derog)

            acc_detail['negative'] = False

            try:
                if acc['Tradeline']['DisputeFlag']['symbol'] == "F":
                    acc_detail['disputed'] = False
                else:
                    acc_detail['disputed'] = True
            except KeyError:
                acc_detail['disputed'] = False


            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat is True or debt is True:
                neg_reason = nega_reason(acc['Tradeline']['PayStatus']['description'].lower(),ttl_late,stat,debt)
                equifax['negative'] += 1
                acc_detail['negative'] = False
                acc_detail['negative_reason'] = neg_reason

            if acc_detail['account_name'] in equifax['account_history'].keys():
                equifax['account_history'][acc_detail['account_name']].append(acc_detail)
                # equifax['account_history'].append(acc_detail)
            else:
                # print("at else")
                equifax['account_history'][acc_detail['account_name']] = []
                equifax['account_history'][acc_detail['account_name']].append(acc_detail)


            equifax['positive'] = int(equif_acc_summary['TotalAccounts']) - equifax['negative']
            equifax['bureau'] = bureau
            # equifax['total_accounts'] = int(equif_acc_summary['TotalAccounts'])
            # equifax['delinquent_accounts'] = int(equif_acc_summary['DelinquentAccounts'])
            # equifax['derogatory_accounts'] = int(equif_acc_summary['DerogatoryAccounts'])
    
            # try:
            #     equifax['no_of_inq'] = int(inq_summary['Equifax']['NumberInLast2Years'])
                
            # except:
            #     pass
            # equifax['no_of_pub_record'] = int(pub_rec_summary['Equifax']['NumberOfRecords'])
            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['credit_score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['credit_score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['credit_score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except:
                pass
            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'y':
                equifax['summary']['account_summary']['no_of_collection'] +=1

            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['accountTypeSymbol'].lower() == 'r':
            #     equifax['revolving_credit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['Tradeline']['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
            #     equifax['credit_card_balance'] += int(acc['Tradeline']['currentBalance'])
                


        elif bureau.lower() == 'transunion':
            
            # transunion['account_history'].append(acc_detail)
            if len(tmp_derog) > 0:
                if tmp_derog not in transunion['derogatory']:
                    transunion['derogatory'].append(tmp_derog)

            acc_detail['negative'] = False

            try:
                if acc['Tradeline']['DisputeFlag']['symbol'] == "F":
                    acc_detail['disputed'] = False
                else:
                    acc_detail['disputed'] = True
            except KeyError:
                acc_detail['disputed'] = False


            if acc['Tradeline']['PayStatus']['description'].lower() == 'collection/chargeoff' or ttl_late > 0 or stat == True or debt == True:
                neg_reason = nega_reason(acc['Tradeline']['PayStatus']['description'].lower(),ttl_late,stat,debt)
                transunion['negative'] += 1
                acc_detail['negative'] = True
                acc_detail['negative_reason'] = neg_reason


            if acc_detail['account_name'] in transunion['account_history'].keys():
                transunion['account_history'][acc_detail['account_name']].append(acc_detail)
                # equifax['account_history'].append(acc_detail)
            else:
                # print("at else")
                transunion['account_history'][acc_detail['account_name']] = []
                transunion['account_history'][acc_detail['account_name']].append(acc_detail)



            transunion['positive'] = int(trns_acc_summary['TotalAccounts']) - transunion['negative']
            transunion['bureau'] = bureau
            # transunion['total_accounts'] = trns_acc_summary['TotalAccounts']
            # transunion['delinquent_accounts'] = trns_acc_summary['DelinquentAccounts']
            # transunion['derogatory_accounts'] = trns_acc_summary['DerogatoryAccounts']
            # try:
            #     transunion['no_of_inq'] = int(inq_summary['TransUnion']['NumberInLast2Years'])
            #     transunion['no_of_pub_record'] = int(pub_rec_summary['TransUnion']['NumberOfRecords'])
            # except Exception as e:
            #     pass

            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['credit_score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['credit_score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['credit_score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except:
                pass
            acc_type = acc['accountTypeSymbol']
            if acc_type.lower() == 'y':
                transunion['summary']['account_summary']['no_of_collection'] +=1
            
            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['accountTypeSymbol'].lower() == 'r':
            #     transunion['revolving_credit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            
            # if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o' and acc['Tradeline']['GrantedTrade']['AccountType']['symbol'].lower() == 'cc':
            #     transunion['credit_card_balance'] += int(acc['Tradeline']['currentBalance'])
    print("left report")
    return transunion,equifax,Experian
    print(equifax)




# path_json = "D:/Codistan/codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/WALTER KNAPP92.json"

# print(json2dict(path_json))