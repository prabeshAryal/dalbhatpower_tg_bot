import json
from fuzzywuzzy import fuzz


class GOTRA(object):
    def __init__(self):
        with open("NEPAL/gotra/all_gotra‌_nep.json", "r", encoding="utf-8") as file:
            self.json_data = json.load(file)

    def search_for_gotra(self, key):
        """
        Search for keys in the JSON data and return associated values.

        Args:
        - key: Key to search for

        Returns:
        - List of values associated with the matching key
        """
        values_found = []
        for k, v_list in self.json_data.items():
            if fuzz.partial_ratio(k, key) >= 80:
                values_found.extend(v_list)
        return values_found

    def search_for_thar(self, value):
        """
        Search for values in the JSON data.

        Args:
        - value: Value to search for

        Returns:
        - List of keys containing the value
        """
        keys_containing_value = []
        for k, v_list in self.json_data.items():
            for v in v_list:
                if fuzz.partial_ratio(v, value) >= 80:
                    keys_containing_value.append(k)
                    break  # Assuming we need to find each key only once
        return keys_containing_value

    def retrieve_all_sahagotris(self, query):
        """
        Retrieve contents based on the query.

        Args:
        - query: Query to retrieve contents

        Returns:
        - Dictionary containing matching keys and their values
        """
        contents = {}
        for k, v_list in self.json_data.items():
            if k == query or query in v_list:
                contents[k] = v_list
        return contents