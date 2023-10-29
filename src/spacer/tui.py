"""The text-based user interface class and it's associated methods.
"""

import sys
import getpass
from spacer import database_connector as sdbc
from spacer import quires as sq

# === GLOBALS ===
from spacer.globals import _spacer_logo, _connection_config_default_params, \
    _default_key_bindings, _console_prompt_text

# === FUNCTIONS ===

# === CLASSES ====


class SpacerTUI():
    """The Text-based User Interface of spacer
    """

    def __init__(self):
        """Constructor of the class: define variables
        """

        # Set default values for parameters
        self.uinput: str = ''
        self.ustack: str = ''  # This is used to emulate a two-element stack of uinnput
        self.config_params: dict = {}

    # === METHODS ===
    def disp(self, message: str) -> int:
        """Method for displaying messages
        """
        sys.stdout.write(message + '\n')
        sys.stdout.flush()
        return 0

    def dict_disp(self,
                  disp_header: str,
                  disp_dict: dict,
                  skip_val_list: list = []) -> int:
        """Simple routine to display dict values nicely
        """

        self.disp('=================')
        self.disp(disp_header)
        self.disp('-----------------')

        for key, val in disp_dict.items():
            if key not in skip_val_list:
                self.disp('{0:s} : {1:s}'.format(str(key), str(val)))

        self.disp('=================')

        return 0

    def console(self, stack_update=True) -> int:
        """The TUI 'console' implementation as a class method
        """
        # First, update the stack (for now limited to a single entry)
        if stack_update:
            self.ustack = self.uinput

        self.uinput = input(_console_prompt_text)

        return 0

    def get_passwd(self) -> str:
        """Similar to the `console` method but more secure for password input
        """
        self.disp("Please provide your password:")
        return getpass.getpass(_console_prompt_text)

    def load_from_stack(self) -> int:
        """Overwrite uinput with the ustack value
        """
        self.uinput = self.ustack

        return 0

    def quit(self) -> int:
        """Method to close the TUI and so spacer
        """
        self.disp(
            '\nSee you cowgirl,\nsomeday, somewhere.')  # A reference to cowboy beboop I guess...
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
            self.dict_disp(disp_header='Spacer help:',
                           disp_dict=_default_key_bindings)

            self.uinput = self.ustack

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
            disable_yn: bool = False) -> int:
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
        return 0

    def check_configuration(self) -> int:
        """Checking if configuration file exist and offer creation if not found
        """
        self.disp('Checking configuration ...')

        if sdbc.check_configuration_file() == False:
            self.start_config_file_creation()
        else:
            self.config_params.update(sdbc.get_config_dict_from_file())

            self.dict_disp(disp_header='DB connection configuration',
                           disp_dict=self.config_params,
                           skip_val_list=sdbc.connection_config_display_skip(
                               self.config_params))

        return 0

    def init_config_file(self) -> int:
        """Code gathering the user config file parameters from the user
        """

        config_params_dict = {}

        for key, val in _connection_config_default_params.items():
            # Handle password separately
            if key == 'password':
                self.uinput = self.get_passwd()
            else:
                self.get_uinput_with_message(
                    message="Please specify '{0:s}'".format(
                        str(key)), def_val=str(val))

            config_params_dict[str(key)] = self.uinput

        self.config_params.update(config_params_dict)

        return 0

    def start_config_file_creation(self) -> int:
        """Top level code to generate a config file
        """
        self.disp('No configuration file found!')
        self.disp('Would you like to create config file now?')

        if self.yes_no_interface():
            self.disp('Creating config file ...')
            self.init_config_file()

            self.dict_disp(disp_header='Selected DB setup parameters',
                           disp_dict=self.config_params)

            sdbc.create_config_file(self.config_params)

            return 0

        else:
            self.quit()

    def connect_to_DB(self) -> int:
        """
        """
        self.disp('Connecting to database ...')

        try:
            sq.connect_to_pstgress_DB(self.config_params)
        except BaseException:
            if sdbc.check_password() == False:
                self.disp('Invalid configuration ...')
                self.quit()
            else:
                wrong_passwd_counter = 3
                while wrong_passwd_counter != 0:
                    try:
                        self.config_params['password'] = self.get_passwd()
                        sq.connect_to_pstgress_DB(self.config_params)
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
                            '2': "Database '{0:s}' does not exist".format(
                                self.config_params['dbname']),
                            '3': 'Unexpected bug'})

                    self.disp(
                        'Please try again, check your database configuration \
    or raise an error on GitHub!')

                    self.quit()

                else:
                    self.disp(
                        'Would you like to configure password storage now?')

                    if self.yes_no_interface():
                        sdbc.set_upasswd(self.config_params['password'])
                        self.disp('Your password has been configured.')

        self.disp('Connected to database')

        return 0

    def boot(self) -> int:
        """Runs when starting spacer
        """
        self.disp(_spacer_logo)
        self.check_configuration()
        self.connect_to_DB()
        return 0


# === MAIN ===
if __name__ == "__main__":
    pass
