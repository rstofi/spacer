"""Command-line app master script
"""

import sys

from spacer import tui as Stui
from spacer import utils as Sutils


def run_spacer_TUI_app() -> int:
    """Main wrapper to run the spacer app in the command line
    """

    app = Stui.SpacerTUI()

    # Initialize the app
    app.boot()

    # Main loop
    while True:
        app.console()
        app.check_for_default_key_bindings()

        exit()

    return 0

def main() -> int:
    """I can later add options here (i.e. run spacer with arguments without TUI)
    """
    run_spacer_TUI_app()

    return 0
   
# === MAIN ===
if __name__ == "__main__":
    main()
