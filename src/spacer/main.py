"""The top-level script that calls the `app` module
"""

import sys

from spacer.tui_engine import SpacerApp, _MDotException


def run_spacer() -> None:
    """Main wrapper to run the spacer app
    """

    app = SpacerApp()

    # Initialize the app
    app.boot()

    # Main loop
    while True:
        try:
            app.console()
            app.check_for_default_key_bindings()
        except Exception as e:
            e_type, e_value, e_traceback = sys.exc_info()

            # --- handle breaking out from sub-routines
            if isinstance(e, Exception) == isinstance(_MDotException(), _MDotException):                
                continue

            # --- handle unexpected errors
            app.disp("An unexpected error occurred:")
            #print(e_type, e_value, e_traceback)
            print(f'{e_type} : {e_value}')
            app.disp("Exiting spacer ...")
            app.quit()


def main() -> None:
    """I can later add options here (i.e. run spacer with arguments without TUI)
    """
    run_spacer()


# === MAIN ===
if __name__ == "__main__":
    main()
