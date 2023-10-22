"""The text-based user interface class and it's associated methods.
"""

from spacer import utils as Sutils

# ===Import globals
from spacer.globals import _config_default_params

# === Functions ===
def close_tui() -> int:
    """
    """

    print('See ya, spacer!') #A reference to cowboy beboop I guess...
    exit()

def chenck_enter(userinput) -> bool:
    """
    """
    if userinput == '':
        return True
    else:
        return False

def yes_no_interface() -> bool:
    """
    """ 
    while True:
        answer = input('> ')

        if answer.lower() in ['yes', 'y']:
            return True
        elif answer.lower() in ['no', 'n']:
            return False
        else:
            print('Please select [Y/n]')

def init_config_file() -> dict:
    """
    """
    config_params = {}

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
        """
        """

        print(Sutils.get_logo())
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
                close_tui()

        #Check the connection to postgres based on the config file parameters
        print('Checking DB connection ...')



        #Sutils.check_database_connection()




# === MAIN ===
if __name__ == "__main__":
    pass