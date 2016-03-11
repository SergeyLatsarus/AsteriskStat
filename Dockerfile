############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Maintaner Name

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl vim wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip libmysqlclient-dev

# Copy the application folder inside the container
RUN git clone https://github.com/SergeyLatsarus/AsteriskStat.git

RUN touch /AsteriskStat/config.py /AsteriskStat/mysqlconfig.py

RUN echo -e "__author__ = 'akr0bat'\nCSRF_ENABLED = True\nSECRET_KEY = 'you-will-never-guess'" >> /AsteriskStat/config.py

RUN echo -e "__author__ = 'akr0bat'\nmysql = {'host': '192.168.88.191',\n'user': 'asteriskstat',\n'passwd': 'lagartos12#',\n'db': 'asteriskcdrdb'}\nuse_anonymous = True" >> /AsteriskStat/mysqlconfig.py

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
