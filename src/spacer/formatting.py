"""Common and utility functions for formatting some markdown reports and some
strings passed to the TUI engine.
"""

import os
import markdown

# === FUNCTIONS
def md_linebreak() -> str:
    """Markdown linebreak: 2 spaces + linebreak
    """
    return "  " + os.linesep
    
def md_par() -> str():
    """New markdown paragraph
    """
    return md_linebreak() + md_linebreak()

def md_inline_image(fig_path:str) -> str:
    """
    """
    return "![Image]({0:s})".format(fig_path) + md_linebreak()

def save_report(report:str, md_report_file:str) -> None:
    """
    """
    # Save in markdown
    report_file = open(md_report_file, "w")
    report_file.write(report)
    report_file.close()

    # Save in html
    report_file = open(os.path.splitext(md_report_file)[0]+'.html', "w")
    report_file.write(markdown.markdown(report,
                    extensions=['markdown.extensions.tables']))
    report_file.close()



# === MAIN ===
if __name__ == '__main__':
    pass