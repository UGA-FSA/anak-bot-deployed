import json
from googleapiclient.errors import HttpError
from auth import service

config = json.loads(open("tempConfig.json").read())

def anon_append(time, data):
    try:
        spreadsheet_id = config["anon"] 

        range_ = 'B:B' 
        value_input_option = 'RAW'
        insert_data_option = 'OVERWRITE' 

        # value_range_body = [[now.strftime("%m/%d/%Y, %H:%M:%S")],[self.ANON_MESSAGE.value]]

        value_range_body = {

            "majorDimension": "COLUMNS",
            "range": "B:B",
            "values": [[time], [data], ["DISCORD"]]

            }   

        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
        request.execute()  
        
    except HttpError as err:
        print(err)