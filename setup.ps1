# Create virtual environment
python -m venv .venv

# Activate and install requirements
# The activate script sets paths for current session, but in PS scripts we can also call the executable directly
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Virtual environment created and dependencies installed."
