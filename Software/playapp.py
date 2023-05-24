import subprocess

# Define la ruta al archivo de la aplicación Streamlit
streamlit_file = 'Software/DashboardV2.py'

# Ejecuta el comando streamlit run
subprocess.run(['streamlit', 'run', streamlit_file])