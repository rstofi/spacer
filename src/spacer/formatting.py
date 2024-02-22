"""Common and utility functions for formatting some markdown reports and some
strings passed to the TUI engine.
"""

import os
import markdown
from urllib.parse import urlparse

# === FUNCTIONS


def md_linebreak() -> str:
    """Markdown linebreak: 2 spaces + linebreak
    """
    return "  " + os.linesep


def md_par() -> str():
    """New markdown paragraph
    """
    return md_linebreak() + md_linebreak()


def md_inline_image(fig_path: str) -> str:
    """
    """
    return f"![Image]({fig_path})" + md_linebreak()


def save_report(report: str, md_report_file: str) -> None:
    """
    """
    # Save in markdown
    report_file = open(md_report_file, "w")
    report_file.write(report)
    report_file.close()

    # Save in html
    report_file = open(os.path.splitext(md_report_file)[0] + '.html', "w")
    report_file.write(
        markdown.markdown(
            report,
            extensions=['markdown.extensions.tables']))
    report_file.close()

def soft_url_validation(url_string:str) -> bool:
    """Validate if a string is url. Or at least generally formatted as

    For more info, see:
        https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
        https://docs.python.org/3/library/urllib.parse.html
        https://docs.python.org/3/library/urllib.parse.html#url-parsing-security

    NOTE: for the streings we need the `hhtps//:` scheme

    """
    try:
        result = urlparse(url_string)
        return all([result.scheme, result.netloc])
    except:
        return False

# === MAIN ===
if __name__ == '__main__':
    pass
