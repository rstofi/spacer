"""Wrappers around SQL quires and postgress connection and so on.
"""

import psycopg2

# === FUNCTIONS ===


def connect_to_pstgress_DB(config_params: dict) -> None:
    """
    """

    # Convert config_params dict to string
    conn_string = ""

    for key, val in config_params.items():
        if key == 'port':
            if val != str(None):
                conn_string += r"{0:s}='{1:s}' ".format(key, val)
            else:
                continue
        else:
            conn_string += r"{0:s}='{1:s}' ".format(key, val)

    # Connect to the database
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    # Here is the problem: I need to connect every time I call a function...
    # and so I should do so. Basically this is beacuse I want to make a minimal viable
    # data product and it seems non-trivial to have a single connection established
    # with my current TUI class sctructure

    # Need a check connection function (this basically) that generates a connection string
    # Then each time a function needs

    # NO fuck it look at this:
    # https://stackoverflow.com/questions/74511042/one-connection-to-db-for-app-or-a-connection-on-every-execution

    conn.close()

    # === PLAN
    # I will need a test connection that is being called from TUI
    # I will need a database class which I can use to interact with the database
    # This I can create at the app.py level via generating a connection string from the TUI app or something....
    # Then I can have TUI functions with the database class provided as an
    # argument


# === MAIN ===
if __name__ == "__main__":
    pass
