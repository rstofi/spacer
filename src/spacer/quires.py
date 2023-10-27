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
    if upasswd != None:
        conn_string += "password='{0:s}'".format(upasswd)

    print(conn_string)

    #Connect to database
    conn = psycopg2.connect(conn_string)

    print(type(conn))
    print(conn)

    return 0


# === MAIN ===
if __name__ == "__main__":
    pass
