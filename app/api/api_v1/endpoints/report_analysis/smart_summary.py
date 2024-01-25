# Extract and transform data to the desired format
def formatdata(data):
    bureaus = ["TransUnion", "Experian", "Equifax"]
    formatted_data = {
        "TransUnion": {
            "account_history": {}
        },
        "Experian": {
            "account_history": {}
        },
        "Equifax": {
            "account_history": {}
        }
    }
    for bureau in bureaus:
      for account_name, entries in data[bureau]["account_history"].items():
          formatted_data[bureau]["account_history"][account_name] = [
              {
                  "account_number": entry["account_number"],
                  "negative": entry["negative"]
              } for entry in entries
          ]

    return formatted_data


# import json

# # Sample JSON data for the old and new versions
# old_data = '''
# {
#    "Equifax":{
#       "account_history":{
#          "IF PR INC":[
#             {
#                "account_number":"56340009456",
#                "negative":false
#             },
#             {
#                "account_number":"56340034562",
#                "negative":false
#             }
#          ]
#       }
#    }
# }
# '''

# new_data = '''
# {
#    "Equifax":{
#       "account_history":{
#          "IF PR INC":[
#             {
#                "account_number":"56340009456",
#                "negative":true
#             }
#          ]
#       }
#    }
# }
# '''

# Load JSON data
#old_json = json.loads(old_data)
#new_json = json.loads(new_data)
# old_json = formatdata(data)
# new_json = formatdata(data1)

# Counter variables
num_updated_negatives = 0
num_deleted_accounts = 0

# Compare negative status and missing accounts
def compare_account_history(old, new):
    global num_updated_negatives
    global num_deleted_accounts

    for bureau, old_accounts in old.items():
        if bureau in new:
            new_accounts = new[bureau]["account_history"]
            for account_type, old_entries in old_accounts["account_history"].items():
                if account_type in new_accounts:
                    new_entries = new_accounts[account_type]
                    for old_entry in old_entries:
                        # Check if account number is present in both old and new
                        account_number = old_entry["account_number"]
                        new_entry = next((entry for entry in new_entries if entry["account_number"] == account_number), None)
                        if new_entry:
                            # Check if negative status has been updated
                            if old_entry["negative"] != new_entry["negative"]:
                                num_updated_negatives += 1
                                # print(f"Account {account_number} has updated negative status.")
                        else:
                            num_deleted_accounts += 1
                            # print(f"Account {account_number} is present in old but not in new.")
    return num_updated_negatives, num_deleted_accounts

# Perform the comparison
# compare_account_history(old_json, new_json)

# # Print the counts
# print(f"Number of negatives that turned positive: {num_updated_negatives}")
# print(f"Number of deleted accounts: {num_deleted_accounts}")
