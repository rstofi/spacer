"""The text-based user interface class and it's associated methods.
"""

import sys
from spacer import utils as Sutils

# === GLOBALS ===
from spacer.globals import _spacer_logo, _config_default_params,\
                            _default_key_bindings

# === FUNCTIONS ===

# === CLASSES ====
class SpacerTUI():
    """The Text-based User Interface of spacer
    """

    def __init__(self):
        """Constructor of the class: define variables
        """

        # Set default values for parameters
        self.uinput:str = ''
        self.config_params:dict = {}

        #self.status:str = 'boot' #This, i might need in the future

    # === METHODS ===
    def disp(self, message:str) -> int:
        """Method for displaying messages
        """
        sys.stdout.write(message + '\n')
        sys.stdout.flush()
        return 0

    def dict_disp(self, disp_header:str, disp_dict:dict) -> int:
        """Simple routine to display dict values nicely
        """

        self.disp('=================')
        self.disp(disp_header)
        self.disp('-----------------')

        for key, val in disp_dict.items():
            self.disp('{0:s} : {1:s}'.format(str(key), str(val)))

        self.disp('=================')

        return 0

    def console(self) -> str:
        """The TUI 'console' implementation as a class method
        """
        self.uinput = input('spacer:> ')
        return self.uinput

    def quit(self) -> int:
        """Method to close the TUI and so spacer
        """
        self.disp('\nSee you cowgirl,\nsomeday, somewhere.') #A reference to cowboy beboop I guess...
        exit()

    def check_for_default_key_bindings(self) -> bool:
        """Defining some default key bindings that can be used at any time.
        These are:
            - q or Q: exiting the app
            - h or H: displaying help message
        """
        # Checking for exit
        if self.uinput.lower() == 'q':
            self.quit()

        # Checking for help
        if self.uinput.lower() == 'h':
            self.dict_disp(disp_header = 'Spacer help:',
                disp_dict = _default_key_bindings)

            return True

        return False 

    def chenck_enter(self) -> bool:
        """Checking if the user input is an enter
        """
        if self.uinput == '':
            return True
        else:
            return False

    def yes_no_interface(self) -> bool:
        """Method for handling [Y/n] questions
        """ 
        while True:
            self.console()
            if self.uinput.lower() in ['yes', 'y']:
                return True
            elif self.uinput.lower() in ['no', 'n']:
                return False
            elif self.check_for_default_key_bindings():
                continue
            else:
                self.disp('Please select [Y/n]')

    def get_uinput_with_message(self, message:str, def_val:str=None) -> int:
        """Simple wrapper to a TUI dialogue that asks for an input
        """
        while True:
            self.disp(message + " (Press enter for default: {0:s})".format(str(def_val)))
            self.check_for_default_key_bindings()
            self.uinput = self.console()

            if self.chenck_enter():
                self.uinput = def_val
                break
            else:
                self.disp('Are you sure? [Y/n]')
                if self.yes_no_interface():
                    break
        return 0

    def check_configuration(self) -> int:
        """Checking if configuration file exist and offer creation if not found
        """
        self.disp('Checking configuration ...')

        if Sutils.check_configuration_file() == False:
            self.start_config_file_creation()
        else:
            self.config_params.update(Sutils.get_config_dict_from_file())

            self.dict_disp(disp_header = 'DB connection configuration',
                            disp_dict = self.config_params)

        return 0

    def init_config_file(self) -> dict:
        """Code gathering the user config file parameters from the user
        """

        config_params_dict = {}

        for key, val in _config_default_params.items():
            self.get_uinput_with_message(message = \
                    "Please specify your {0:s} name".format(str(key)),
                    def_val = str(val))

            config_params_dict[str(key)] = self.uinput

        return config_params_dict

    def start_config_file_creation(self) -> int:
        """Top level code to generate a config file
        """
        self.disp('No configuration file found!')
        self.disp('Would you like to create config file now?')

        if self.yes_no_interface():
            self.disp('Creating config file ...')
            config_params_dict = self.init_config_file()

            self.dict_disp(disp_header = 'Selected DB setup parameters',
                            disp_dict = config_params_dict)

            Sutils.create_config_file(config_params_dict)

            return 0

        else:
            self.quit()

    def boot(self) -> int:
        """Runs when starting spacer
        """
        self.disp(_spacer_logo)
        self.check_configuration()
        return 0

# === MAIN ===
if __name__ == "__main__":
    pass