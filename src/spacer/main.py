"""The top-level script that calls the `app` module
"""

import sys

from spacer.app import SpacerApp


def run_spacer() -> int:
    """Main wrapper to run the spacer app
    """

    app = SpacerApp()

    # Initialize the app
    app.boot()

    # Main loop
    while True:
        app.console()
        app.check_for_default_key_bindings()

        #exit()

    return 0


def main() -> int:
    """I can later add options here (i.e. run spacer with arguments without TUI)
    """
    run_spacer()

    return 0


# === MAIN ===
if __name__ == "__main__":
    main()
