# PeakDB

Provides a database of the highest earth peaks !

## Install

- Python 3.7+ is mandatory
- Linux only (here with CentOS)

### Prerequesite: install and run MongoDB

- Install and run MongoDB : <https://docs.mongodb.com/manual/administration/install-on-linux/>
- Install and run Docker: <https://docs.docker.com/engine/install/centos/>
- Install Docker-compose: <https://docs.docker.com/compose/install/>

### Procedure

Back:

```bash
cd server/
yum install virtualenvwrapper
mkvirtualenv -p python3 peakdb
workon peakdb
pip install -r requirements.txt
python setup.py install
cd ..
```

Front:

```bash
cd front/
npm install
cd ..
```

## Development usage

### Run the servers

```bash
python server/peakdb/app.py
```
Served at <localhost:5000/peaks>

Optionally , a front Vue server is available :
```bash
cd front/
npm run serve
```
Front pages are available at <localhost:8080> and <localhost:8080/peaks>

### Run the tests

```bash
pytest server/tests
```

## Docker setup

```bash
sudo docker-compose up
```
