FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install --upgrade setuptools 
RUN pip install -r server/requirements.txt
RUN cd server && python setup.py install
CMD python server/src/app.py