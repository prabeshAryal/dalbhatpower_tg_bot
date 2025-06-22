import requests,os
import json


RASIFAL = os.environ.get('RASIFAL')
from fuzzywuzzy import fuzz

class NepaliRashiFal():   
    @staticmethod
    def get_index(input_string):        
        # See maybe if it's already in the index
        try:
            a = int(input_string.split(' ')[0])
            a = a - 1 
            return a if (a>=0 and a<=11) else -1
        except ValueError as e:
            # print('Rashifal Script :  Input is a string, So, we will check further' + str(e))
            
            def find_rashi_index_nepali(bolamaya):
                rashifal_list = [
                {'rashi': 'मेष', 'initials': 'चु, चे, चो, ला, लि, लु, ले, लो, अ', 'typos': {'मेस', 'मेश', 'मे्श'}},
                {'rashi': 'वृष', 'initials': 'इ, उ, ए, ओ, वा, वि, वु, वे, वो', 'typos': {'वृषा', 'वृष्', 'वृष', 'वृषी', 'वृषि'}},
                {'rashi': 'मिथुन', 'initials': 'का, कि, कु, घ, ङ, छ, के, को, हा', 'typos': {'मिठुन','मिथून', 'मिठन', 'मिथन', 'मीथुन', 'मीथून'}},
                {'rashi': 'कर्कट', 'initials': 'हि, हु, हे, हो, डा, डि, डु, डे, डो', 'typos': {'कर्क', 'कटक', 'कर्कड', 'कर्कटः', 'कर्कडः', 'कटकः'}},
                {'rashi': 'सिंह', 'initials': 'मा, मि, मु, मे, मो, टा, टि, टु, टे', 'typos': {'सिं', 'सिंहः', 'सींह', 'सीं', 'सींहः'}},
                {'rashi': 'कन्या', 'initials': 'टो, पा, पि, पु, ष, ण, ठ, पे, पो', 'typos': {'कन्य', 'कन्याः', 'कन्यू', 'कन्यूः'}},
                {'rashi': 'तुला', 'initials': 'रा, रि, रु, रे, रो, ता, ति, तु, ते', 'typos': {'तूला', 'तुल', 'तूल', 'तुलाः', 'तूलाः', 'तुलः', 'तूलः'}},
                {'rashi': 'वृश्चिक', 'initials': 'तो, ना, नि, नु, ने, नो, या, यि, यु', 'typos': {'वृश्चिका', 'वृश्चिकः', 'वृश्चिकि', 'वृश्चिकी'}},
                {'rashi': 'धनु', 'initials': 'ये, यो, भा, भि, भु, धा, फा, ढा, भे', 'typos': {'धनुः', 'धनुस्', 'धनू', 'धनूः'}},
                {'rashi': 'मकर', 'initials': 'भो, जा, जि, जु, जे, जो, ख, खि, खु, खे, खो, गा, गि', 'typos': {'मकड', 'मकरः', 'मकरि', 'मकरी'}},
                {'rashi': 'कुम्भ', 'initials': 'गु, गे, गो, सा, सि, सु, से, सो, दा', 'typos': {'कुम्भः', 'कुम्भः', 'कुम्भि', 'कुम्भी'}},
                {'rashi': 'मीन', 'initials': 'दि, दु, थ, झ, ञ, दे, दो, चा, चि', 'typos': {'मिन','मिनः', 'मीनः', 'मीनः', 'मीनि', 'मीनी'}}
            ]
                for index, rashi_data in enumerate(rashifal_list):
                    rashi_name = rashi_data['rashi']
                    if bolamaya == rashi_name or bolamaya in rashi_data['typos']:
                        return index
                    
                for index, rashi_data in enumerate(rashifal_list):
                    initials_list = rashi_data['initials'].split(', ')
                    if bolamaya[0] in ''.join(initials_list):
                        return index
                    
                return 'unmacthed'

            def find_rashi_index_english(string):
                def find_matching_index(input_str, target_list):
                    threshold = 90
                    for idx, target_str in enumerate(target_list):
                        if fuzz.partial_ratio(input_str.lower(), target_str.lower()) > threshold:
                            return idx
                    return 'unmacthed'

                horoscope_list = [
                'mesh aries',
                'brishabha vrisav taurus',
                'mithun gemini',
                'karkat cancer',
                'simha singh leo',
                'kanya virgo kanye',
                'tula libra',
                'vrishchik brischik scorpio',
                'dhanu sagittarius dhanush',
                'makar capricorn mkar',
                'kumbh kumv aquarius kumbha',
                'meen pisces min'
            ]


                matching_index = find_matching_index(string, horoscope_list)
                return(matching_index)
            nep_index_return = find_rashi_index_nepali(input_string)
            eng_index_return = find_rashi_index_english(input_string)
            if nep_index_return != 'unmacthed':
                return(nep_index_return)
            elif eng_index_return != 'unmacthed':
                return (eng_index_return)
            else:
                return -2
    
    def get_horoscope(tapaiko_rashi):
        if tapaiko_rashi.lower()=='ganesh' or tapaiko_rashi.lower() == 'samisha' or tapaiko_rashi.lower() == 'gunace' or tapaiko_rashi.lower() == 'jayant' or tapaiko_rashi.lower() == 'admin' or tapaiko_rashi.lower() == 'dilasha' or tapaiko_rashi.lower() == 'dilase' or tapaiko_rashi.lower() == 'dilashe' or tapaiko_rashi.lower() == 'dilse' or tapaiko_rashi.lower() == 'dils':
            return "Dilasha", 8000
        rashi_index=NepaliRashiFal.get_index(tapaiko_rashi)
        if rashi_index >=0 and rashi_index <= 11:
            api_resp = requests.get(RASIFAL)
            neededinfo = json.loads(api_resp.json()['list'][0]['value'])
            
            if rashi_index == 11:
                rashikofal = neededinfo['items'][rashi_index]['desc'].split('\r')[0]
                                    
            this_will_be_returned = f'''
            मिति : *{neededinfo['date']}*\n
            राशि : ***{neededinfo['items'][rashi_index]['rashi']}***\n\nअक्षर : *{neededinfo['items'][rashi_index]['initials']}* \n
            \nराशिफल : {neededinfo['items'][rashi_index]['desc'] if rashi_index<11 else rashikofal}
            '''
            return this_will_be_returned, rashi_index
        elif rashi_index == -1:
            return "Please enter value in proper range [1-12].", 69
        elif rashi_index == -2:
            return "No such horoscope exists.", 69

    def get_all_horoscope():
        api_resp = requests.get(RASIFAL)
        neededinfo = json.loads(api_resp.json()['list'][0]['value'])
        string = 'आज मिति **{}**को राशिफल । \n\n'.format(neededinfo['date'])
        for item in neededinfo['items']:
            rashi_index=NepaliRashiFal.get_index(item['rashi'])
            if rashi_index == 11:
                rashikofal = neededinfo['items'][rashi_index]['desc'].split('\r')[0]
            else :
                rashikofal = neededinfo['items'][rashi_index]['desc']
            string += '***' + item['rashi'] + ': ***' + '\n' + '\t' + '_'+item['initials']+'_'+'\n'+'`'+rashikofal+'`'+'\n\n'
        return(string)

# print(NepaliRashiFal.get_all_horoscope())
