import sys
import os

# Make the project root importable so we can pull in dashboard.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard import server as app  # noqa: E402  (Vercel looks for a WSGI "app")
