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

from spacer.database import create_empty_db

# === GLOBALS ===
from spacer.globals import SPACER_LOGO, DEFAULT_KEY_BINDINGS, DEFAULT_SCHEMA_PATH, \
            CONSLOLE_PROMPT_TEXT, EXIT_MESSAGE, PROJECT_ROOT, DEAFAULT_DB_PATH


# === PATHS ===
# Append the project root to sys.path
sys.path.append(PROJECT_ROOT) 

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
        self.db_path = None
        self.db_connection = None # sqlite3.Connection object
        self.cursor = None # squlite.Cursor object

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

    def load_from_stack(self) -> None:
        """Overwrite uinput with the ustack value
        """
        self.uinput = self.ustack

    def quit(self) -> None:
        """Method to close the TUI and so spacer
        """
        self.disp(EXIT_MESSAGE)  # A reference to cowboy beboop I guess...
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

    def configure(self, database_path:str = None) -> None:
        """Configure spacer database and the Database Handler.

        """

        # If the user is providing a custom database path
        if database_path != None:
            # Check if database exists
            if os.path.isfile(db_path):
                self.db_path = database_path
            else:
                raise ValueError('Database not found: {0:s}'.format(database_path))
                # Here I can add a call for creating the database

        # Else, use the default settings
        else:
            # Check if database dir and database exists and if not create it
            if not os.path.isfile(DEAFAULT_DB_PATH):
                # Create database
                self.disp('Creating default database ...')
                create_empty_db(DEAFAULT_DB_PATH, DEFAULT_SCHEMA_PATH)

            # Set database path
            self.db_path = DEAFAULT_DB_PATH

        self.disp("Using database: {0:s}".format(self.db_path))

    def boot(self, database_path:str = None) -> None:
        """Runs when starting spacer
        """
        self.disp(SPACER_LOGO)
        self.configure(database_path)


# === MAIN ===
if __name__ == "__main__":
    pass
