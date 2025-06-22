from mytelegrammodules.commandhandlers.commonimports import *

class DBMSSimple():

    def get_relative_directory_path():
        # Get the path of the current script (the file where this function is defined)
        current_script_path = os.path.abspath(__file__)

        # Get the directory part of the file path
        relative_directory_path = os.path.dirname(current_script_path)

        return relative_directory_path
      
    
    def update_data(chatid, texter, username, group):

        db_file_path = os.path.join(DBMSSimple.get_relative_directory_path(),'db.json')

        # Read the existing data from the database file or create an empty dictionary if the file is empty
        try:
            with open(db_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {}

        # Check if the given chatid already exists in the data
        if chatid in data:
            # If chatid exists, update the corresponding values
            data[chatid]['fullname'] = texter
            data[chatid]['username'] = username
            data[chatid]['group'] = group
        else:
            # If chatid doesn't exist, add a new entry with the provided data
            data[chatid] = {'fullname': texter, 'username': username, 'group': group}

        # Write the updated data back to the database file
        with open(db_file_path, 'w') as file:
            json.dump(data, file)

# Example usage:
# update_data(1234, 'John Doe', 'johndoe123', 'Group A')


# print(DBMSSimple.get_relative_directory_path())