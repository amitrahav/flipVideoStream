# pull official base image
FROM python:3.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update
RUN apt-get install libgtk2.0-dev -y

# install software dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./flaskr /usr/src/app/

# copy initial
COPY ./startDocker.sh ./
RUN chmod +x /usr/src/app/startDocker.sh

EXPOSE 5000

CMD [ "/usr/src/app/startDocker.sh" ]
