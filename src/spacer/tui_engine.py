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

from spacer.database_handler import DatabaseHandler, create_empty_db

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
    # === METHODS ===
    def __init__(self):
        """Constructor of the class: define variables
        """

        # Set default values for parameters
        self.uinput: str = ''
        self.ustack: str = ''  # This is used to emulate a two-element stack of uinnput
        self.db_path = None
        self.db_handler = None # spacer.database_handler: DatabaseHandler

    # === Core TUI methods
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

    def get_bool_input_with_message(
            self,
            message: str) -> bool:
        """Simple wrapper for getting a boolean input
        """
        self.disp(message)
        return self.yes_no_interface()

    def get_uinput_with_message(
            self,
            message: str,
            def_val: str = None,
            enable_yn: bool = False) -> None:
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

            if enable_yn:
                self.disp('Are you sure? [y/n]')
                if self.yes_no_interface():
                    break
            else:
                break

    # === Config and boot methods

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


    def connect_to_db(self) -> None:
        """
        """
        
        self.disp("Connecting to database ...")

        if self.db_path == None:
            raise ValueError("No database set!")

        # Create handler
        self.db_handler = DatabaseHandler(self.db_path)

        # Connect to db
        self.db_handler.create_db_connection()


    def load_views(self) -> None:
        """
        """

        self.disp("Loading views ...")

    def boot(self, database_path:str = None) -> None:
        """Runs when starting spacer
        """
        self.disp(SPACER_LOGO)
        self.configure(database_path)
        self.connect_to_db()
        self.load_views()

        # Show hint for usage by default
        self.disp("For help/manual press 'h'")
        self.disp("")

    # === Core event loop methods

    def quit(self) -> None:
        """Method to disconnect db, close the TUI and so spacer
        """
        self.db_handler.close_db_connection()
        self.disp(EXIT_MESSAGE)  # A reference to cowboy beboop I guess...
        exit()

    def show_help(self) -> None:
        """
        """
        self.dict_disp(disp_header='Spacer manual:',
                       disp_dict=DEFAULT_KEY_BINDINGS)

        self.uinput = self.ustack

    def run_sql_script(self) -> None:
        """
        """

        # Get sql script and store it in uinput

        self.get_uinput_with_message( message = 'Provide path to sql script:')

        sql_script_path = self.uinput

        # Open the sql file
        if not os.path.isfile(self.uinput):
            self.disp('File not found: {0:s}'.format(self.uinput))
        else:
            self.db_handler.execute_sql_file(self.uinput)

        # Need to display the results (if any)

        # THIS IS A TO DO

    def get_new_company_dict(self, new_company_dict:dict) -> dict:
        """
        """
        # Check if the input dict only has a name
        if list(new_company_dict.keys()) != ['name']:
            print(new_company_dict)
            print(new_company_dict.keys())
            raise ValueError("Invalid company dict provided!")

        # Is recruiter agency
        new_company_dict['is_recruitment_agency'] = self.get_bool_input_with_message(
            message = 'Is the company a recruitment agency? [y/n]')

        # Company website
        self.get_uinput_with_message( message = 'Company website:')
        new_company_dict['website'] = self.uinput
        
        # Company website
        self.get_uinput_with_message( message = 'Comments on company:')
        new_company_dict['comments'] = self.uinput

        return new_company_dict

    def start_new_job_application(self) -> None:
        """
        """

        # Add a new company first
        new_company_dict = {}

        # Get the company name
        self.get_uinput_with_message( message = 'Company name:')
        new_company_dict['name'] = self.uinput

        # Check if this company already exists or not
        if self.db_handler.check_if_company_exists(new_company_dict['name']) == False:

            new_company_dict = self.get_new_company_dict(new_company_dict)

            self.dict_disp(disp_header="New company to add:", disp_dict=new_company_dict)

            if self.get_bool_input_with_message(message="Are you sure to add this company?"):
                self.db_handler.add_company(new_company_dict)
        else:
            self.disp("Company '{0:s}' already exists in database ...".format(
                new_company_dict['name']))

    # === MAIN event loop engine
    def check_for_default_key_bindings(self) -> bool:
        """THIS is basically te main function, the core of the event loop

        Defining some default key bindings that can be used at any time.
        These are defined in the `globals` module and currently are:
            - q or Q: exiting the app
            - h or H: displaying help message
            - s or S: Start new job application (and add it to the database)
            - i or I: Add new interview
            - u or U: Update application status
            - r or R: Run SQL file (all commands from the file)
        """

        is_default_key = True

        # Checking for exit
        if self.uinput.lower() == 'q':
            self.quit()

        # Checking for help
        elif self.uinput.lower() == 'h':
            self.show_help()

        # Checking for running sql file
        elif self.uinput.lower() == 'r':
            self.run_sql_script()

        # Checking for new application status
        elif self.uinput.lower() == 's':
            self.start_new_job_application()

        else:
            is_default_key = False
    
        return is_default_key

# === MAIN ===
if __name__ == "__main__":
    pass
