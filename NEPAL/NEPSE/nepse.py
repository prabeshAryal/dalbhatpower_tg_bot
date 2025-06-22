# import requests,os,ast

from mytelegrammodules.commandhandlers.commonimports import *

NEPSE_API = os.environ.get('NEPSE')

class NepalStock():
        
    def find_stock_id(response, input_info):
        for stock in response:
            if (
                input_info.lower() in stock["companyName"].lower()
                or input_info.lower() in stock["symbol"].lower()
                or input_info.lower() in stock["securityName"].lower()
                or input_info.lower() in stock["companyEmail"].lower()
                or input_info.lower() in stock["website"].lower()
            ):
                return stock["id"]

        return None
    def format_key(key):
        key_mapping = {
            "id":"ID",
        "securityId": "Security ID",
        "openPrice": "Open Price",
        "highPrice": "High Price",
        "lowPrice": "Low Price",
        "totalTradeQuantity": "Total Trade Quantity",
        "totalTrades": "Total Trades",
        "lastTradedPrice": "Last Traded Price",
        "previousClose": "Previous Close",
        "businessDate": "Business Date",
        "closePrice": "Close Price",
        "fiftyTwoWeekHigh": "52 Weeks High",
        "fiftyTwoWeekLow": "52 Weeks Low",
        "lastUpdatedDateTime": "Last Updated",
        "securityName": "Security",
        "permittedToTrade": "Permitted to Trade",
        "companyName": "Company Name",
        "symbol": "SYMBOL",
        "companyEmail": "Company Email",
        "website": "Website",
        "sectorName": "Sector Name",
        "regulatoryBody": "Regulatory Body",
        "instrumentType": "Instrument Type",
        "activeStatus": "Active Status",
    }
        return key_mapping.get(key, key)
    
    def format_datetime(timestamp):
        dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_dt = dt.strftime("%I:%M:%S %p\n\t\t\t\t\t\t\t\t\t   %B %d, %A, %Y")
        return formatted_dt
    
    def nepse_indexes():
        response = requests.get(NEPSE_API)
        data=ast.literal_eval(response.text)

       # Create the NEPSE Update heading
        markdown_string = "***NEPSE Update***\n\n"

        # Add each index information
        for index_data in data:
            index_name = index_data["index"]
            current_value = index_data["currentValue"]
            change = index_data["change"]
            percentage_change = index_data["perChange"]

            # Format the data in Markdown
            index_info = f"{index_name}\n\t\t\t\t\t\t➜{current_value:.2f}\n\t\t_Change : {change:.2f} ({percentage_change:.2f}%)_\n"
            markdown_string += f"- {index_info}\n"
        return markdown_string
    
    def nepse_single_stock(symbol):
        isymbolnum = symbol.isdigit() if isinstance(symbol, str) else str(symbol).isnumeric()
        if isymbolnum == False:
            print(symbol + " is not num , so checking if it exists.")
            response1 = requests.get(NEPSE_API+'company/list')
            if response1.status_code != 200:
                print(symbol + " is does not exist")
                return 'Would you mind sending in proper format?'
            company_list=ast.literal_eval(response1.text)
            id=NepalStock.find_stock_id(company_list,symbol)
            if id == None:
                return 'Please recheck your Symbol or Company Name'
            print(symbol+' exists as id : ' + str(id))
        else:
            id = symbol
        
        response2 = requests.get(NEPSE_API+'security/'+str(id))
        response2.status_code           
        def format_dict(data, prefix="", indent_level=0):
            indent = "\t" * indent_level
            formatted = f"\n{indent}***{prefix}***\n"
            for key, value in data.items():
                if isinstance(value, dict):
                    formatted += format_dict(value, key, indent_level + 1)
                else:
                    if key == "lastUpdatedDateTime":
                        value = NepalStock.format_datetime(value)
                    formatted += f"{indent}- {NepalStock.format_key(key)}: {value}\n"
            return formatted


        if response2.status_code == 200:
            formatted = format_dict(response2.json())
            formatted = '‎ \n ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ⚡️***NEPSE Live***⚡️' + formatted
            formatted = formatted.replace('securityMcsData','Floor Chart :')
            formatted = formatted.replace('securityData','Stock Information :')         
            return formatted
        return 'Please Type the correct Security ID Number'
        
        
        


# print(NepalStock.nepse_indexes())
