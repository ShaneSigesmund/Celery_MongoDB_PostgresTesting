%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python3.10 -m venv venv
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org install wheel
venv\Scripts\python -m pip --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org install -r requirements.txt
venv\Scripts\activate
