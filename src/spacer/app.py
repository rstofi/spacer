"""Command-line app master script
"""

import sys

from spacer import tui as Stui
from spacer import utils as Sutils

def main() -> int:
    """
    """
    app = Stui.SpacerTUI()

    # Initialize the app
    app.boot()
    app.check_configuration()

    # Main loop
    while True:
        app.console()
        app.default_key_bindings()

        exit()

    return 0

# === MAIN ===
if __name__ == "__main__":
    main()
