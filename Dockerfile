FROM python:3.9-slim

WORKDIR /usr/src
COPY ./requirements.txt . 
RUN pip install -r requirements.txt 

COPY . . 

CMD ["python", "output.py"]

