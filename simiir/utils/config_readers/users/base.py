from lxml import etree
from simiir.utils.config_readers import ConfigReaderError
from simiir.utils.config_readers.base_config_reader import BaseConfigReader
from simiir.utils.config_readers.users.search_user_reader import SearchUserConfigReader
from simiir.utils.config_readers.users.conversational_config_reader import ConversationalUserConfigReader
import importlib
import pkgutil
import inspect

# Replace user_types using reflection of the users subpackage - loop through each module, find a class in the module, and check for the attribute type_name.
# The type_name is the key of the dictionary, and the class name is the value.
# This will allow for easier extension of the user subpackage.
user_types = {
    'SearchUser': SearchUserConfigReader,
    'ConversationalUser': ConversationalUserConfigReader
}



class UserConfigReader(BaseConfigReader):

    def __init__(self, config_filename=None, dtd_filename=None):
        super(UserConfigReader, self).__init__(config_filename=config_filename, dtd_filename=dtd_filename)
    
    @staticmethod
    def get_user_types():
        user_types = {}

        package = importlib.import_module('simiir.utils.config_readers.users')
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            # Import the module
            module = importlib.import_module(modname)
            # Append the module to the list
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__:
                    if hasattr(obj, 'user_type'):
                        user_types[obj.user_type] = obj
        
        return user_types

    @staticmethod
    def get_user_config_reader(config_filename=None):
        user_types = UserConfigReader.get_user_types()

        if config_filename is None:
            raise ConfigReaderError("No configuration file has been specified.")
        else:
            config_file = etree.parse(config_filename)
        
        if 'type' in config_file.getroot().attrib:
            user_type = config_file.getroot().attrib['type']
        else:
            raise ConfigReaderError(f"No user type specified in configuration file {config_filename}.")

        if user_type not in user_types.keys():
            raise ConfigReaderError(f"User type {user_type} not recognised.")
        
        return user_types[user_type](config_filename=config_filename)