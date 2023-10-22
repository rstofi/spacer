"""Global variables
"""

import os

# Absolute path to the configuration path
global _config_path
_config_path = os.path.join(os.path.expanduser('~'),'.spacer.ini')

# Default configuration file parameters
global _config_default_params

_config_default_params = {'dbname' : 'spacer_job_board',
                'user' : 'postgres',
                'host' : 'localhost',
                'port' : None}