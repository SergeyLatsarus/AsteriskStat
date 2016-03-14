############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Sergey Latsarus

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl vim wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip libmysqlclient-dev

RUN pip install MySQL-python
RUN pip install simple_salesforce

# Copy the application folder inside the container
RUN git clone https://github.com/SergeyLatsarus/AsteriskStat.git

COPY ./config.py /AsteriskStat/config.py
COPY ./mysqlconfig.py /AsteriskStat/mysqlconfig.py
COPY ./salesforce_config.py /AsteriskStat/salesforce_config.py

# Get pip to download and install requirements:
RUN pip install -r /AsteriskStat/requirements.txt

# Expose ports
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /AsteriskStat

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python run.py
