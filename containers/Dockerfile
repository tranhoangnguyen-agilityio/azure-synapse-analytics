FROM mcr.microsoft.com/azure-cli
# https://hub.docker.com/_/microsoft-azure-cli

RUN apk add git
RUN apk add openrc openssh

RUN mkdir ~/.ssh
RUN ssh-keyscan github.com > ~/.ssh/known_hosts

WORKDIR /usr/src/app
COPY option1 ./option1
COPY option2 ./option2

# Install requiremnts.txt
RUN pip install -r option1/src/requirements.txt

CMD ["bash"]