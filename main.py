import subprocess
import sys

def run_streamlit_app():
    try:
        # Check if streamlit is installed
        subprocess.run([sys.executable, "-m", "pip", "show", "streamlit"], check=True, capture_output=True)
        print("Streamlit is installed. Starting the app...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app/app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Streamlit is not installed or could not be run. Please install it using: pip install streamlit")
        print(f"Details: {e.stderr.decode()}")
    except FileNotFoundError:
        print("Error: 'streamlit' command not found. Make sure Streamlit is installed and in your PATH.")

if __name__ == "__main__":
    run_streamlit_app()
