import urllib.request
import sys

try:
    response = urllib.request.urlopen("http://localhost:8000/health", timeout=5)
    if response.getcode() == 200:
        sys.exit(0)
except Exception as e:
    print(f"Health check failed: {e}")
sys.exit(1)
