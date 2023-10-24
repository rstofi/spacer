"""The text-based user interface class and it's associated methods.
"""

import sys
from spacer import utils as Sutils

# ===Import globals
from spacer.globals import _config_default_params

# === Functions ===
def init_config_file() -> dict:
    """
    """
    config_params = {}


    return config_params

    #Get the database name
    while True:
        print("Please specify your database name (press enter for default: \
'{0:s}'):".format(_config_default_params['dbname']))
        answer = input()

        if chenck_enter:
            answer = _config_default_params['dbname']
            break
        else:
            print('Are you sure? [Y/n]]')
            if yes_no_interface():
                break

    config_params['dbname'] = answer

    #Get the postgres user name
    while True:
        print("Please specify your postgres user name (press enter for default: \
'{0:s}'):".format(_config_default_params['user']))
        answer = input()

        if chenck_enter:
            answer = _config_default_params['user']
            break
        else:
            print('Are you sure? [Y/n]]')
            if yes_no_interface():
                break

    config_params['user'] = answer

    #Get the host name
    while True:
        print("Please specify your host name (press enter for default: \
'{0:s}'):".format(_config_default_params['host']))
        answer = input()

        if chenck_enter:
            answer = _config_default_params['host']
            break
        else:
            print('Are you sure? [Y/n]]')
            if yes_no_interface():
                break

    config_params['host'] = answer
    
    #Get the port
    while True:
        print("Please specify your port (press enter for default: \
'{0:s}'):".format(str(_config_default_params['port'])))
        answer = input()

        if chenck_enter:
            answer = _config_default_params['port']
            break
        else:
            print('Are you sure? [Y/n]]')
            if yes_no_interface():
                break

    config_params['port'] = answer

    # Summarize the config file:
    print('\nYour config file have been set up with the following parameters: \n')
    print('dbname: {0:s}'.format(config_params['dbname']))
    print('user: {0:s}'.format(config_params['user']))
    print('host: {0:s}'.format(config_params['host']))
    print('port: {0:s}\n'.format(str(config_params['port'])))

    return config_params

# === CLASSES ====
class SpacerTUI():
    """The Text-based User Interface of spacer
    """

    def __init__(self):
        """Constructor of the class: define variables
        """

        # Set default values for parameters
        self.status = 'boot'
        self.uinput = None

        # Print logo
        #print(Sutils.get_logo())
        
        """
        print('Checking configuration ...')

        #Look for configuration file
        if Sutils.check_configuration_file() == False:
            print('No configuration file found!')
            print('Would you like to create config file now?')

            if yes_no_interface():
                config_params = init_config_file()
                print('Creating config file ...')
                Sutils.create_config_file(config_params)
            else:
                self.close_tui()

        #Check the connection to postgres based on the config file parameters
        print('Checking DB connection ...')
        """

        #Sutils.check_database_connection()

        #exit()

    # === METHODS ===
    def disp(self, message) -> int:
        """Method for displaying messages
        """
        sys.stdout.write(message + '\n')
        sys.stdout.flush()
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

    def default_key_bindings(self) -> int:
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
            self.disp(Sutils.get_help_message())

        return 0 

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
            else:
                self.default_key_bindings()
                self.disp('Please select [Y/n]')

    def boot(self) -> int:
        """Runs when starting spacer
        """
        self.disp(Sutils.get_logo())
        return 0

    def check_configuration(self) -> int:
        """Checking if configuration file exist and offer creation if not found
        """
        self.disp('Checking configuration ...')

        if Sutils.check_configuration_file() == False:
            self.create_config_file()

        return 0

    def create_config_file(self) -> int:
        """
        """
        self.disp('No configuration file found!')
        self.disp('Would you like to create config file now?')

        if self.yes_no_interface():
            self.disp('Creating config file ...')
            config_params = init_config_file()

            #Sutils.create_config_file(config_params)

            return 0

        else:
            self.quit()

# === MAIN ===
if __name__ == "__main__":
    pass