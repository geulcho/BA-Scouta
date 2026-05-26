import sys
import os

# Add root directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app
