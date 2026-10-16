import subprocess
import sys

def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installiere fehlendes Paket: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
