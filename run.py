#!/usr/bin/env python3
"""
Ansari Email Builder Runner
Checks dependencies and launches the Streamlit app
"""

import sys
import subprocess

def check_and_install_deps():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import yaml
        import jinja2
        print("All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please run manually:")
            print("pip install -r requirements.txt")
            return False

def main():
    print("Ansari Email Builder - Starting up...")

    # Test core functionality first
    print("\n1. Testing core functionality...")
    try:
        result = subprocess.run([sys.executable, "utils/test_builder.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("   Core functionality: OK")
        else:
            print("   Core functionality: FAILED")
            print(result.stdout)
            print(result.stderr)
            return
    except Exception as e:
        print(f"   Core test failed: {e}")
        return

    # Check dependencies
    print("\n2. Checking dependencies...")
    if not check_and_install_deps():
        return

    # Launch Streamlit
    print("\n3. Launching Streamlit interface...")
    print("   Opening browser at http://localhost:8501")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        # Run streamlit with inherited stdout/stderr for live log output
        subprocess.run([sys.executable, "-m", "streamlit", "run", "UI Builder.py"],
                      stdout=None, stderr=None)
    except KeyboardInterrupt:
        print("\n\nShutting down Ansari Email Builder.")
    except Exception as e:
        print(f"Failed to launch Streamlit: {e}")
        print("\nTry running manually:")
        print("streamlit run \"UI Builder.py\"")

if __name__ == "__main__":
    main()