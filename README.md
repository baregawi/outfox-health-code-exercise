# outfox-health-code-exercise
Code exercise for Outfox Health

## Docker setup instructions:

### Get the container running on your machine

Start downloading docker for your machine. Then run command the below. It will download postgress from dockerhub if the container is not already on your machine:

```
docker run --name my-postgres -e POSTGRES_PASSWORD=buruk101 -p 5432:5432 -v pgdata:/var/lib/postgresql/data -d postgres
```

### Log into a shell container and instal PostGIS:

Log into a shell on the container:

```
docker exec -it my-postgres /bin/bash
```

Now install PostGIS extension:

```
apt update
apt install postgis
```

Enter 'Y' when prompted. And exit the container when done.

### Log into psql on the container and create database and necessary extensions

To login into the database:

```
docker exec -it my-postgres psql -U postgres
```

Add the database we will be using by running:

```
CREATE DATABASE outfoxhealth;
```

Run `\l` to make sure you see the new database.

Now add the needed extensions:

```
CREATE EXTENSION postgis;
CREATE EXTENSION pg_trgm;
CREATE EXTENSION fuzzystrmatch;
```

## Install dependencies and package, set up venv, and upload data into database:

### Install dependencies and package, and setup venv

Make sure you are using python3.11. Git clone this package to your workspace:

```
git clone https://github.com/baregawi/outfox-health-code-exercise.git
```

Start a venv for this project and activate it:

```
python3.11 -m venv venv
source venv/bin/activate
```

`cd` to the backend directory and install the requirements and the package itself.

```
cd backend
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install ./app
```

### Upload data into database

Upload data into database. Due to the slowness of openstreetmap.org we will only upload the first 500 lines:

```
python3.11 app/accessdata/etl.py
```

## Run server and test out endpoints:

### Run server:

To get the server running locally run the following:

```
python3.11 main.py
```

### Test endpoints:

Enter the following into your browser to test the `/providers` endpoint:

```
http://0.0.0.0:8000/providers?drg_desc=CRANIOTOMY&zipcode=02150&radius=10000
```

Enter the following into your browest to test the `/ask` endpoint:

```
http://0.0.0.0:8000/ask?question=Get+me+providers+with+provider+org+name+equal+to+023
```

I have had issues getting the `/ask` API to produce results. But I am out of time.


## Architectural decisions:

This was a relatively small project. The biggest thing was that I've mostly been working on C/C++ and C# (Unity) lately. So there weren't really any major architectural decisions due to size. And the focus was just to move fast and get a first version done. I figured I could make things extra pretty or do extra credit work if I finished in time.