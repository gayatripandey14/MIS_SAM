FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /MIS_SAM

WORKDIR /MIS_SAM

COPY requirements.txt /MIS_SAM/


RUN pip install -r requirements.txt
COPY . /MIS_SAM/
# RUN python3 manage.py makemigrations 
# RUN python3 manage.py migrate