import re
import json
import os

class NepaliDictionary():
    def nepali_dictionary(inputNepaliWord):
        # Get the absolute path of the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to test.json
        file_path = os.path.join(current_dir, 'baukodosh.json')

        # Load the JSON data from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # # Function to search for a word in the data and return in the Nepali dictionary format
        # def search_word(word):
        #     results = []
        #     for item in data:
        #         if item.get('word') == word:
        #             word_entry = f"शब्द: {item['word']}\nअर्थहरू:"
        #             for definition in item['definitions']:
        #                 word_entry += f"\n\t{definition['grammar']}"
        #                 for sense in definition['senses']:
        #                     word_entry += f"\n\t\t- {sense}"
        #             results.append(word_entry)
        #     return results
        # Function to search for a word in the data and return in the Nepali dictionary format
        def search_word(word):
            results = []
            for item in data:
                if item.get('word') == word:
                    word_entry = f"शब्द: **{item['word']}**\nअर्थहरू:"
                    for definition in item['definitions']:
                        grammar = definition.get('grammar', '')
                        word_entry += f"\n\t{grammar}"
                        senses = definition.get('senses', [])
                        for sense in senses:
                            word_entry += f"\n\t\t- {sense}"
                    results.append(word_entry)
            return results

        # Search for the word 'अ' (replace with the word you want to search for)
        try :
            results = search_word(inputNepaliWord)[0]
            return results
        except IndexError as e :
            return '_Unfortunately, No such word was found in database._'

# print(NepaliDictionary.nepali_dictionary('म'))