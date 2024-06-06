#Use linux based python image which includes python 
# FROM python:3.10-slim-bullseye
FROM python:3.12-bullseye

#update package index
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests build-essential default-libmysqlclient-dev pkg-config && pip install --no-cache-dir --upgrade pip
#install os dependencies
#     && apt-get install -y --no-install-recommends --no-install-suggests \
#     build-essential default-libmysqlclient-dev \ 
# #upgrade pip to latest version 
#     && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
#we copy the req file and run it before copying the python script so that if we change the code in the 
#script and need to rebuild the image, it will not need to rebuild the layer with the installed python packages.
#only layers after copying the script will be rebuilt
RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

#Expose container port
EXPOSE 5000

#this is the default state/cmd run when the container is launched
CMD ["python3", "server.py"]