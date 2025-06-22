import datetime
import nepali_datetime
import subprocess
from dateutil.parser import parse


class nepalSpecialTimes():
    devanagari_digits = {
            '0': '०',
            '1': '१',
            '2': '२',
            '3': '३',
            '4': '४',
            '5': '५',
            '6': '६',
            '7': '७',
            '8': '८',
            '9': '९',
        }
    
    def is_valid_timestamp(timestamp):
    #     devanagari_to_english = {
    #     '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    #     '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    # }

    #     # Function to convert Devanagari numbers to English numbers
    #     def convert_devanagari_to_english(text):
    #         return ''.join(devanagari_to_english.get(char, char) for char in text)
        
    #     timestamp = convert_devanagari_to_english(timestamp)
        possible_formats = [
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d',
            '%m/%d/%Y',
            '%m/%d/%y',
            '%d/%m/%Y',
            '%d/%m/%y',
            '%d-%m-%Y',
            '%d-%m-%y',
            '%m-%d-%Y',
            '%m-%d-%y',
            '%Y-%m-%d',
            '%f/%e/%Y',
            '%f/%e/%y',
            '%e/%f/%Y',
            '%e/%f/%y',
            '%f-%e-%Y',
            '%f-%e-%y',
            '%e-%f-%Y',
            '%e-%f-%y',
            '%b %e, %Y',
            '%B %e, %Y',
            '%b %d, %Y',
            '%B %d, %Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %I:%M:%S %p',
            '%Y-%m-%d %I:%M:%S %p',
              # Add more formats if needed
        ]

        for date_format in possible_formats:
            try:
                datetime_object = nepali_datetime.datetime.strptime(timestamp, date_format)
                return datetime_object, date_format
            except ValueError:
                pass

        # If none of the formats match, return an indication
        return None, "Format not recognized"

            
    def convert_to_nepali_time(time_str):

        am_pm_mapping = {
            'AM': 'बिहान',
            'PM': 'बेलुका',
        }

        def to_devanagari_digits(text):
            return ''.join(nepalSpecialTimes.devanagari_digits.get(char, char) for char in text)

        def to_nepali_am_pm(text):
            return am_pm_mapping.get(text, text)

        devanagari_time = to_devanagari_digits(time_str)
        nepali_time = devanagari_time.replace('AM', to_nepali_am_pm('AM')).replace('PM', to_nepali_am_pm('PM'))

        return nepali_time



    def nepali_now():
        string1 = f''' \t***{nepalSpecialTimes.convert_to_nepali_time(nepali_datetime.datetime.now().strftime('%I:%M:%S %p'))}***\n***{nepali_datetime.date.today().strftime('%K %N %D, %G')}***'''
        
        string2 = f'''\n\n\t*{nepali_datetime.datetime.now().strftime('%I:%M:%S %p')}*\n{datetime.date.today().strftime('%A, %B %d, %Y')}\n\t{nepali_datetime.date.today().strftime('%d %B, %Y B.S.')}'''
        return string1+string2

        
    def nepali_today():
        string = f'''\t***{nepali_datetime.date.today().strftime('%K %N %D, %G')}***\n{nepali_datetime.date.today().strftime('%d %B, %Y B.S.')}\n\n\t *{datetime.date.today().strftime('%A, %B %d, %Y')}* \n'''
        return string
        
    def patro():

        try:
            # Execute the nepali_datetime command and capture the output
            output = subprocess.check_output(
                ["python3", "-c", "import nepali_datetime; nepali_datetime.datetime.now().calendar()"],
                text=True
            )
            # return the captured output
            return output

        except subprocess.CalledProcessError as e:
            print("Failure in Calendar Module:", e)
    
    def convert_to_bs(randomstring):
        try:
            def convert_date_to_standard_format(date_str):
            # Parse the input date using dateutil's parser
                parsed_date = parse(date_str, fuzzy=True)

                # Extract year, month, and day from the parsed date
                year = parsed_date.year
                month = parsed_date.month
                day = parsed_date.day

                return [year, month, day]
            YYYY, MM, DD = convert_date_to_standard_format(randomstring)
            
            return '***'+ str(nepali_datetime.datetime.from_datetime_datetime(datetime.datetime(YYYY,MM,DD)).strftime('%K %N %D, %G')) + '***'
        except:
            return 'The format you entered is Invalid'

    def convert_to_ad(randomstring):
        
            # Function to convert Devanagari numbers to English numbers
        datetime_object, detected_format = nepalSpecialTimes.is_valid_timestamp(randomstring)
        
        if datetime_object != None:
            return '***'+ str(nepali_datetime.datetime.to_datetime_date(datetime_object).strftime('%B %m, %Y, %A')) + '***' + '\n\n\t'+'Note : ' + '_This module is incomplete or imperfect. Expect errors, bugs and glitches._'
        else:
            return '_This module is incomplete or imperfect. Expect errors, bugs and glitches._'
            # return 'This Service is not available'

# # a = calendars()
# b= ''
# print(nepalSpecialTimes.convert_to_ad(b))




