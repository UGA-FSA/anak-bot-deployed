import json
from googleapiclient.errors import HttpError
from auth import service
from pprint import pprint

config = json.loads(open("tempConfig.json").read())

def get_member(fullname):
    try:
        spreadsheet_id = config["AKA"] 
        range_ = 'A:Z' 
        value_render_option = 'FORMATTED_VALUE'
        date_time_render_option = 'SERIAL_NUMBER'

        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
        response = request.execute()


        filtered_list = []

        for index, x in enumerate(response['values']):
            firstname = fullname.split()[0].lower()
            if firstname in x[1].lower():
                filtered_list.append(x)

        # pprint(filtered_list)
        return filtered_list
            
# TODO: Change code below to process the `response` dict:
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

