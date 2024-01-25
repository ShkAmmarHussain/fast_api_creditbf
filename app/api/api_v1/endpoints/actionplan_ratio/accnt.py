from datetime import datetime

def details(path_json):

    report = path_json

    accnts = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['TradeLinePartition']
    trns_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['TransUnion']
    equif_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Equifax']
    exper_acc_summary = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Summary']['TradelineSummary']['Experian']


    creditscores = report['BundleComponents']['BundleComponent'][-1]['TrueLinkCreditReportType']['Borrower']['CreditScore']


    Experian = {
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

    equifax = {
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


    transunion = {
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



    for creditscore in creditscores:
        if creditscore['Source']['Bureau']['description'].lower() == 'Experian':
            Experian['Credit Score'] = creditscore['riskScore']
        elif creditscore['Source']['Bureau']['description'].lower() == 'transunion':
            transunion['Credit Score'] = creditscore['riskScore']
        elif creditscore['Source']['Bureau']['description'].lower() == 'equifax':
            equifax['Credit Score'] = creditscore['riskScore']


    for acc in accnts:
        ageinyears = 0
        try:
            temp_age = datetime.strptime(acc['Tradeline']['dateReported'], "%Y-%m-%d") - datetime.strptime(acc['Tradeline']['dateOpened'], "%Y-%m-%d")
        except TypeError:
            temp_age = datetime.strptime(acc['Tradeline'][-1]['dateReported'], "%Y-%m-%d") - datetime.strptime(acc['Tradeline'][-1]['dateOpened'], "%Y-%m-%d")
        except:
            temp_age = datetime.strptime(acc['Tradeline']['dateReported'], "%Y-%m-%d") - datetime.strptime(acc['Tradeline']['dateAccountStatus'], "%Y-%m-%d")

        ageinyears = temp_age.days // 365

        ttl_late = 0

        try:
            late = acc['Tradeline']['GrantedTrade']
            ttl_late = int(late['late90Count']) + int(late['late60Count']) + int(late['late30Count'])
        except:
            ttl_late = 0


        if type(acc['Tradeline']) == type([]):
            acc['Tradeline'] = acc['Tradeline'][0]

        try:
            bureau = acc['Tradeline']['bureau']
        except:
            bureau = str(acc['Tradeline'][8]['bureau'])

        coll_detail = []
        coll_detail.append(ageinyears)
        coll_detail.append(acc['Tradeline']['accountNumber'])
        coll_detail.append(acc['Tradeline']['creditorName'])
        coll_detail.append(acc['Tradeline']['PayStatus']['description'])
        coll_detail.append(acc['Tradeline']['currentBalance'])
        if acc['Tradeline']['AccountCondition']['symbol'].lower() == 'p':
            coll_detail.append("Paid")
        else:
            coll_detail.append("-")
        try:
            coll_detail.append(acc['Tradeline']['CollectionTrade']['originalCreditor'])
        except KeyError:
            coll_detail.append('-')
        

        chrgoff = []
        if "chargeoff" in acc['Tradeline']['PayStatus']['description'] and acc['Tradeline']['currentBalance'] != 0:
            chrgoff.append(acc['Tradeline']['accountNumber'])
            chrgoff.append(acc['Tradeline']['creditorName'])
            chrgoff.append(acc['Tradeline']['PayStatus']['description'])
            chrgoff.append(acc['Tradeline']['currentBalance'])


        stat = False
        if "Remark" in acc['Tradeline']:
            try:
                if "bankruptcy" in acc['Tradeline']['Remark']['RemarkCode']['description']:
                    stat = True
            except:
                if "bankruptcy" in acc['Tradeline']['Remark'][0]['RemarkCode']['description']:
                    stat = True

        if stat:
            tmp_bnkruptcy = []
            tmp_bnkruptcy.append(acc['Tradeline']['accountNumber'])
            tmp_bnkruptcy.append(acc['Tradeline']['creditorName'])
            try:
                tmp_bnkruptcy.append(acc['Tradeline']['GrantedTrade']['dateLastPayment'])
            except:
                pass

        if bureau.lower() == 'experian':
            if len(chrgoff) != 0:
                Experian['Charge off'].append(chrgoff)
            Experian['Bureau'] = bureau
            Experian['Total Balances'] = int(exper_acc_summary['TotalBalances'])

            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'experian':
                    Experian['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except KeyError:
                Experian['Credit Score'] = 0

            acc_type = acc['accountTypeSymbol']
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                if acc_type.lower() == 'r':
                    Experian['No of open Revolving Acc'] += 1
                elif acc_type.lower() == 'i':
                    Experian['No of open Installment'] +=1
                elif acc_type.lower() == 'y':
                    Experian['No of open Collection Acc'] +=1
                    if len(coll_detail) > 0:
                        Experian['Collection Details'].append(coll_detail)

            # if acc['Tradeline']['AccountCondition']['symbol'].lower() == 'p':
            #     coll_detail.append("Paid")
            #     Experian['Collection Details'].append(coll_detail)

            try:
                Experian['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            except:
                pass

            if stat:
                Experian['Bankruptcy'].append(tmp_bnkruptcy)

            if 'Remark' in acc['Tradeline']:
                if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                    list_of_studentloan = ['student loan','transferred','defaulted','collection']
                    for loan in list_of_studentloan:

                        try:
                            if loan in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                                Experian['Open Student loans'] +=1
                                tmp = []
                                tmp.append(loan)
                                tmp.append(acc['Tradeline']['currentBalance'])
                                if ttl_late > 0:
                                    tmp.append(acc['Tradeline']['accountNumber'])
                                    tmp.append(acc['Tradeline']['GrantedTrade']['PayStatusHistory']['startDate'])
                                    tmp.append(acc['Tradeline']['PayStatus']['description'])
                                    tmp.append(acc['Tradeline']['creditorName'])
                                    Experian['Loan Details'].append(tmp)

                        except:
                            if loan in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                                Experian['Open Student loans'] +=1
                                tmp = []
                                tmp.append(loan)
                                tmp.append(acc['Tradeline']['currentBalance'])
                                if ttl_late > 0:
                                    tmp.append(acc['Tradeline']['accountNumber'])
                                    tmp.append(acc['Tradeline']['GrantedTrade']['PayStatusHistory']['startDate'])
                                    tmp.append(acc['Tradeline']['PayStatus']['description'])
                                    tmp.append(acc['Tradeline']['creditorName'])
                                    Experian['Loan Details'].append(tmp)


        elif bureau.lower() == 'equifax':
            if len(chrgoff) != 0:
                equifax['Charge off'].append(chrgoff)
            equifax['Bureau'] = bureau
            equifax['Total Balances'] = int(equif_acc_summary['TotalBalances'])

            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'equifax':
                    equifax['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except KeyError:
                equifax['Credit Score'] = 0


            acc_type = acc['accountTypeSymbol']
            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                if acc_type.lower() == 'r':
                    equifax['No of open Revolving Acc'] += 1
                elif acc_type.lower() == 'i':
                    equifax['No of open Installment'] +=1
                elif acc_type.lower() == 'y':
                    equifax['No of open Collection Acc'] +=1
                    if len(coll_detail) > 0:
                        equifax['Collection Details'].append(coll_detail)

            if acc['Tradeline']['AccountCondition']['symbol'].lower() == 'p':
                coll_detail.append("Paid")
                equifax['Collection Details'].append(coll_detail)

            try:
                equifax['Credit Limit'] += int(acc['Tradeline']['GrantedTrade']['CreditLimit'])
            except:
                pass


            if stat:
                equifax['Bankruptcy'].append(tmp_bnkruptcy)


            if 'Remark' in acc['Tradeline']:
                if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                    list_of_studentloan = ['student loan','transferred','defaulted','collection']
                    for loan in list_of_studentloan:


                        try:
                            if loan in acc['Tradeline']['Remark']['RemarkCode']['description'].lower():
                                equifax['Open Student loans'] +=1
                                tmp = []
                                tmp.append(loan)
                                tmp.append(acc['Tradeline']['currentBalance'])
                                if ttl_late > 0:
                                    tmp.append(acc['Tradeline']['accountNumber'])
                                    tmp.append(acc['Tradeline']['GrantedTrade']['PayStatusHistory']['startDate'])
                                    tmp.append(acc['Tradeline']['PayStatus']['description'])
                                    tmp.append(acc['Tradeline']['creditorName'])
                                    equifax['Loan Details'].append(tmp)
                        except:
                            if loan in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                                equifax['Open Student loans'] +=1
                                tmp = []
                                tmp.append(loan)
                                tmp.append(acc['Tradeline']['currentBalance'])
                                if ttl_late > 0:
                                    tmp.append(acc['Tradeline']['accountNumber'])
                                    tmp.append(acc['Tradeline']['GrantedTrade']['PayStatusHistory']['startDate'])
                                    tmp.append(acc['Tradeline']['PayStatus']['description'])
                                    tmp.append(acc['Tradeline']['creditorName'])
                                    equifax['Loan Details'].append(tmp)


        elif bureau.lower() == 'transunion':
            if len(chrgoff) != 0:
                transunion['Charge off'].append(chrgoff)
            transunion['Bureau'] = bureau
            transunion['Total Balances'] = trns_acc_summary['TotalBalances']

            try:
                if report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-4]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-3]['CreditScoreType']['riskScore'])
                if report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['Source']['Bureau']['description'].lower() == 'transunion':
                    transunion['Credit Score'] = int(report['BundleComponents']['BundleComponent'][-2]['CreditScoreType']['riskScore'])
            except KeyError:
                transunion['Credit Score'] = 0

            acc_type = acc['accountTypeSymbol']

            if acc['Tradeline']['OpenClosed']['symbol'].lower() == 'o':
                if acc_type.lower() == 'r':
                    transunion['No of open Revolving Acc'] += 1
                elif acc_type.lower() == 'i':
                    transunion['No of open Installment'] +=1
                elif acc_type.lower() == 'y':
                    transunion['No of open Collection Acc'] +=1
                    if len(coll_detail) > 0:
                        transunion['Collection Details'].append(coll_detail)

            if acc['Tradeline']['AccountCondition']['symbol'].lower() == 'p':
                coll_detail.append("Paid")
                transunion['Collection Details'].append(coll_detail)

            if stat:
                transunion['Bankruptcy'].append(tmp_bnkruptcy)

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
                                tmp = []
                                tmp.append(loan)
                                tmp.append(acc['Tradeline']['currentBalance'])
                                if ttl_late > 0:
                                    tmp.append(acc['Tradeline']['accountNumber'])
                                    tmp.append(acc['Tradeline']['GrantedTrade']['PayStatusHistory']['startDate'])
                                    tmp.append(acc['Tradeline']['PayStatus']['description'])
                                    tmp.append(acc['Tradeline']['creditorName'])
                                    transunion['Loan Details'].append(tmp)

                        except:
                            if loan in acc['Tradeline']['Remark'][0]['RemarkCode']['description'].lower():
                                transunion['Open Student loans'] +=1
                                tmp = []
                                tmp.append(loan)
                                tmp.append(acc['Tradeline']['currentBalance'])
                                if ttl_late > 0:
                                    tmp.append(acc['Tradeline']['accountNumber'])
                                    tmp.append(acc['Tradeline']['GrantedTrade']['PayStatusHistory']['startDate'])
                                    tmp.append(acc['Tradeline']['PayStatus']['description'])
                                    tmp.append(acc['Tradeline']['creditorName'])
                                    transunion['Loan Details'].append(tmp)


    return transunion,equifax,Experian
    print(Experian)


# path_json = "D:/Codistan/CreditButterfly/Credit_Reports/Credit_report_SmartCredit_json/LINDA GRIMM52.json"

# details(path_json)