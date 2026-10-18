import sys
import webbrowser
import threading
import time
import uvicorn

def open_browser(port: int = 8000):
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"\n🚀 Opening EchoPrism in your browser: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")

if __name__ == "__main__":
    port = 8000
    if "--streamlit" in sys.argv:
        print("Launching Streamlit interface...")
        import subprocess
        subprocess.run(["streamlit", "run", "streamlit_app.py"])
    else:
        print("=" * 65)
        print("⚡ EchoPrism: PR & Media Intelligence Information Overload Eliminator")
        print("=" * 65)
        print(f"Server running at: http://localhost:{port}")
        print("Press Ctrl+C to stop the server.")
        print("=" * 65)
        
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()
        uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False)
