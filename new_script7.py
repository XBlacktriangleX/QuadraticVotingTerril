
import subprocess
from pyngrok import ngrok

# Beende alle vorherigen ngrok-Prozesse, um sicherzustellen, dass nur ein Tunnel läuft
!pkill ngrok

# Start Streamlit app
subprocess.Popen(["streamlit", "run", "app.py"])

# Create ngrok tunnel
public_url = ngrok.connect(8501)
print(f"Öffne die Streamlit App hier: {public_url}")
