"""Wrappers around SQL quires and postgress connection and so on.
"""

import psycopg2

# === FUNCTIONS ===
def connect_to_pstgress_DB(config_params:dict, upasswd:str=None) -> int:
    """
    """

    # Convert config_params dict to string 
    conn_string = ""

    for key, val in config_params.items():
        if key == 'port':
            if val != str(None): 
                conn_string += r"{0:s}='{1:s}' ".format(key,val)
            else:
                continue
        else:
            conn_string += r"{0:s}='{1:s}' ".format(key,val)

    # If password is provided by the user
    # TO DO: remove this bit when password storage from file implemented on top level and this case is handled
    if upasswd != None:
        conn_string += "password='{0:s}'".format(upasswd)
    else:
        RaiseValueError('No password provided!')

    print(conn_string)

    #Connect to the database
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    print('AAAAAAAA')

    # Here is the problem: I need to connect every time I call a function...
    # and so I should do so. Basically this is beacuse I want to make a minimal viable
    # data product and it seems non-trivial to have a single connection established
    # with my current TUI class sctructure

    # Need a check connection function (this basically) that generates a connection string
    # Then each time a function needs

    # NO fuck it look at this: https://stackoverflow.com/questions/74511042/one-connection-to-db-for-app-or-a-connection-on-every-execution

    #conn.close()

    return 0


# === MAIN ===
if __name__ == "__main__":
    pass
