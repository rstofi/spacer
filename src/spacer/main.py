"""The top-level script that calls the `app` module
"""

import sys

from spacer.tui_engine import SpacerApp


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
            app.disp("An unexpected error occurred")
            print(e)
            app.disp("Exiting spacer ...")
            app.quit()

def main() -> None:
    """I can later add options here (i.e. run spacer with arguments without TUI)
    """
    run_spacer()


# === MAIN ===
if __name__ == "__main__":
    main()
