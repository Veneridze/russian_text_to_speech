FROM python:3.10.0

RUN apt-get update
RUN apt-get install -y python3-dev libasound2-dev curl
RUN curl --proto '=https' --tlsv1.2 -y -sSf https://sh.rustup.rs | sh

# Our Debian with python is now installed.
# Imagine we have folders /sys, /tmp, /bin etc. there
# like we would install this system on our laptop.

RUN mkdir build

# We create folder named build for our stuff.

WORKDIR /build

# Basic WORKDIR is just /
# Now we just want to our WORKDIR to be /build

COPY . .

# FROM [path to files from the folder we run docker run]
# TO [current WORKDIR]
# We copy our files (files from .dockerignore are ignored)
# to the WORKDIR
#--no-cache-dir 
RUN pip3 install -r requirements.txt

# OK, now we pip install our requirements

EXPOSE 8000

# Instruction informs Docker that the container listens on port 80

#WORKDIR /build/app

CMD uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --proxy-headers
