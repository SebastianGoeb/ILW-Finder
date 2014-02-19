import sys
import os.path
import logging

logging.getLogger().setLevel(logging.DEBUG)

# third-party libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

# local modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# templates
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'templates'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../venv/lib/python2.7/site-packages'))
