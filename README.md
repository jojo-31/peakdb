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
python setup.py develop
```

Front:

```bash
cd front/
npm install
```

## Development usage

```bash
python server/src/main.py
cd front/
npm run serve
```

Front is served under localhost:8080
Back under localhost:5000/peaks

## Docker setup

```bash
sudo docker-compose up
```
