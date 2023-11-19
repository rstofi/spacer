"""The top-level class to handle user interface (simple command line input and output)
and the app's main functionalities.

For now this is the core class that handles quite a lot of things, in particular
both the user interface and the configuration and creation of other class instances
and methods.

For now, I keep this quite complex, but I might will try to re-factor it later

"""

import os
import sys
import getpass
from spacer import utils as su
from spacer import quires as sq

# === GLOBALS ===
from spacer.globals import SPACER_LOGO, DEFAULT_KEY_BINDINGS, CONSLOLE_PROMPT_TEXT, \
    CONNECTION_CONFIG_PATH, CONNECTION_CONFIG_DEFAULT_PARAMS

# === FUNCTIONS ===

# === CLASSES ====


class SpacerApp():
    """The Text-based User Interface of spacer
    """

    def __init__(self):
        """Constructor of the class: define variables
        """

        # Set default values for parameters
        self.uinput: str = ''
        self.ustack: str = ''  # This is used to emulate a two-element stack of uinnput
        self.verbose: bool = True  # If True all messages are displayed
        self.connection_config_path = None
        self.connection_config_params: dict = {}

    # === METHODS ===
    def disp(self, message: str) -> None:
        """Method for displaying messages.

        Parameters:
            - message (str): the message displayed in stdout
        """
        sys.stdout.write(message + '\n')
        sys.stdout.flush()

    def dict_disp(self,
                  disp_header: str,
                  disp_dict: dict,
                  skip_val_list: list = []) -> None:
        """Simple routine to display dict values nicely
        """

        self.disp('=================')
        self.disp(disp_header)
        self.disp('-----------------')

        for key, val in disp_dict.items():
            if key not in skip_val_list:
                self.disp('{0:s} : {1:s}'.format(str(key), str(val)))

        self.disp('=================')

    def console(self, stack_update=True) -> None:
        """The TUI 'console' implementation as a class method
        """
        # First, update the stack (for now limited to a single entry)
        if stack_update:
            self.ustack = self.uinput

        self.uinput = input(CONSLOLE_PROMPT_TEXT)

    def get_passwd(self) -> None:
        """Similar to the `console` method but more secure for password input
        """
        self.disp("Please provide your password:")
        return getpass.getpass(CONSLOLE_PROMPT_TEXT)

    def load_from_stack(self) -> None:
        """Overwrite uinput with the ustack value
        """
        self.uinput = self.ustack

    def quit(self) -> None:
        """Method to close the TUI and so spacer
        """
        self.disp(
            '\nSee you cowgirl,\nsomeday, somewhere.')  # A reference to cowboy beboop I guess...
        exit()

    def check_for_default_key_bindings(self) -> bool:
        """Defining some default key bindings that can be used at any time.
        These are defined in the `globals` module and currently are:
            - q or Q: exiting the app
            - h or H: displaying help message
        """
        is_default_key = False

        # Checking for exit
        if self.uinput.lower() == 'q':
            self.quit()

        # Checking for help
        if self.uinput.lower() == 'h':
            self.dict_disp(disp_header='Spacer help:',
                           disp_dict=DEFAULT_KEY_BINDINGS)

            self.uinput = self.ustack
            is_default_key = True

        # Displaying database connection parameters
        if self.uinput.lower() == 'd':
            self.dict_disp(disp_header='DB connection configuration:',
                           disp_dict=self.connection_config_params,
                           skip_val_list=su.connection_config_display_skip(
                               self.connection_config_params))

            self.uinput = self.ustack
            is_default_key = True

        return is_default_key

    def chenck_enter(self) -> bool:
        """Checking if the user input is an enter
        """
        return self.uinput == ''

    def yes_no_interface(self) -> bool:
        """Method for handling [Y/n] questions
        """

        self.console()
        while True:
            if self.uinput.lower() in ['yes', 'y']:
                self.load_from_stack()
                return True
            elif self.uinput.lower() in ['no', 'n']:
                self.load_from_stack()
                return False
            elif self.check_for_default_key_bindings():
                continue
            else:
                self.disp('Please select [Y/n]')
                self.console(stack_update=False)

    def get_uinput_with_message(
            self,
            message: str,
            def_val: str = None,
            disable_yn: bool = False) -> None:
        """Simple wrapper to a TUI dialogue that asks for an input
        """
        while True:
            if def_val is None:
                self.disp(message)
                self.console()
                self.check_for_default_key_bindings()

            else:
                self.disp(
                    message +
                    " (Press enter for default: {0:s})".format(
                        str(def_val)))
                self.console()
                self.check_for_default_key_bindings()

                if self.chenck_enter():
                    self.uinput = def_val
                    break

            if disable_yn:
                break
            else:
                self.disp('Are you sure? [Y/n]')
                if self.yes_no_interface():
                    break

    def configure(self) -> None:
        """Configure spacer general settings.

        If configuration file is not existing, then this routine generates a
        .spacer/ directory under the user's HOME library and a config.ini file
        with the default configuration settings.

        Otherwise, this routine reads from the aforementioned config file and
        loads the connection settings into self.connection_config_params
        """
        spacer_config_params = {}

        # This bit of code should run only once when spacer is ran first time
        if su.check_spacer_configuration_file() == False:

            self.disp('Found no spacer configuration file!')
            self.disp('Creating spacer config file now ...')

            # Connection configuration file location
            self.get_uinput_with_message(
                message="Please provide the desired location for the connection \
configuration file:".format(CONNECTION_CONFIG_PATH),
                def_val=str(CONNECTION_CONFIG_PATH))

            spacer_config_params['connection_config_path'] = self.uinput

            # I can add more parameters here later, that's why I am using a
            # dict

            # Create config file
            self.disp('Creating config file ...')

            su.create_config_file(spacer_config_params)

        else:
            # Get spacer general config params from file
            spacer_config_params.update(su.get_config_dict_from_file())

        # General configuration i.e. setting some of the class attributes
        self.connection_config_path = spacer_config_params['connection_config_path']

    def check_connection_configuration(self) -> None:
        """Checking if the connection configuration file exist and offer it's
        creation if the file is not found.
        """
        if not os.path.isfile(self.connection_config_path):
            self.start_connection_config_file_creation()
        else:
            self.connection_config_params.update(
                su.get_connection_config_dict_from_file(
                    conn_config_path=self.connection_config_path))

    def init_connection_config_file(self) -> None:
        """Code gathering the user config file parameters from the user
        """

        config_params_dict = {}

        for key, val in CONNECTION_CONFIG_DEFAULT_PARAMS.items():
            # Handle password separately
            if key == 'password':
                self.disp(
                    "NOTE: press enter to skip storing your password in the config file!")
                self.uinput = self.get_passwd()
            else:
                self.get_uinput_with_message(
                    message="Please specify '{0:s}'".format(
                        str(key)), def_val=str(val))

            config_params_dict[str(key)] = self.uinput

        self.connection_config_params.update(config_params_dict)

    def start_connection_config_file_creation(self) -> None:
        """Top level code to generate a config file
        """
        self.disp('Found no connection configuration file!')
        self.disp('Would you like to create the connection config file now?')

        if self.yes_no_interface():
            self.disp('Creating config file ...')
            self.init_connection_config_file()

            self.dict_disp(disp_header='Selected DB setup parameters',
                           disp_dict=self.connection_config_params,
                           skip_val_list=su.connection_config_display_skip(
                               self.connection_config_params))

            su.create_connection_config_file(
                self.connection_config_params,
                conn_config_path=self.connection_config_path)

        else:
            self.quit()

    def connect_to_DB(self) -> None:
        """
        """
        self.disp('Connecting to database ...')

        try:
            sq.connect_to_pstgress_DB(self.connection_config_params)
        except BaseException:
            if not su.check_password_exists_in_config():
                self.disp('No password found in connection configuration ...')
            else:
                self.disp(
                    'Invalid configuration or wrong password in connection config file!')

            self.disp('Please provide your password:')
            wrong_passwd_counter = 3
            while wrong_passwd_counter != 0:
                try:
                    self.connection_config_params['password'] = self.get_passwd(
                    )
                    sq.connect_to_pstgress_DB(self.connection_config_params)
                    break

                except BaseException:
                    self.disp('Invalid password ...')

                    wrong_passwd_counter -= 1

            if wrong_passwd_counter == 0:
                self.disp('Unexpected error occurred!')
                self.dict_disp(
                    disp_header='Possible reasons',
                    disp_dict={
                        '1': 'Wrong password provided 3 times',
                        '2': 'Wrong password stored in connection config file',
                        '3': "Database '{0:s}' does not exist".format(
                            self.connection_config_params['dbname']),
                        '4': 'Unexpected bug'})

                self.disp(
                    'Please try again, check your database configuration \
or raise an error on GitHub!')

                self.quit()

        self.disp("Connected to database")

    def boot(self) -> None:
        """Runs when starting spacer
        """
        self.disp(SPACER_LOGO)
        self.configure()
        self.check_connection_configuration()
        self.connect_to_DB()


# === MAIN ===
if __name__ == "__main__":
    pass
