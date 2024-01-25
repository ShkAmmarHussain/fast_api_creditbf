# fast_api_creditbf

### Create virtual env:

conda create -p env_name python==3.* -y

### Activate env:

conda activate env_name

### Install package in the created environment:

pip install -r requirements.txt

### Run fastapi

uvicorn app.main:app --reload --port 5000
