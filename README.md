# tobib.io-api

This is the backend for the AI challenge proposed in the dev fest hackathon That I compted in from 12/12/2023 to 13/12/2023
A link to the challenge premise along side a starter boilerplate code to solve this probleme is found on https://github.com/BIGmama-technology/Community-devfest-2023-challange
I have not used the fastAPI starter code and decided to solve it using the django Rest Framework to develop the API

## Installation

1. Create a python virtual environment

- for a windows machine use the following:

```
python -m venv venv
```

- for a linux machine use the following:

```
python3 -m venv venv
```

2. Activate the virtual environment

- for a windows machine use the following:

```
venv\Scripts\activate
```

- for a linux machine use the following:

```
source venv/bin/activate
```

3. install dependencies

```
pip install -r requirements.txt
```

4. to create the database

```
cd tobib
python manage.py migrate
```

5. To run the server

5.1 Windows

```
run.bat
```

5.2 Linux

```
chmod +x run.sh
run.sh
```

## Setup your API key

1. create a .env file in the tobib folder

2. Inside it provide your api key in the following format

```
HUGGING_FACE_API_TOKEN=YOUR API KEY TOKEN
```

# generate mock data

generate mock data to test different views

```
cd tobib
python populate-db.py
```

# API documentation

to acess the documentation via swagger
go to http://127.0.0.1:8000/swagger/
