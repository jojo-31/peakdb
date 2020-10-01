# PeakDB

Provides a database of the highest earth peaks !

## Install

* Python 3.7+ is mandatory
* Linux only (here with CentOS)

### Prerequesite: install and run MongoDB

<https://docs.mongodb.com/manual/administration/install-on-linux/>

### Procedure

Back:

```bash
cd server/
yum install virtualenvwrapper
mkvirtualenv -p python3 peakdb
workon peakdb
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

Go to localhost:8080 !
