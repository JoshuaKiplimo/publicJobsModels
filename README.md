## Project Run Guide

#### Create environment

- make sure you have python 3.10 installed in virtual env is also installed
- run bellow commands to setup and activat virtual envrinmnet

```bash
cd your_project_root_directory
python -m ven your_env_name
source your_env_name/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- if your project runs of different port than `8000` or your is running in other than local host them you have to specify `host_url` in `.env` file, located in project level root directory
