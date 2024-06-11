FROM mcr.microsoft.com/azure-cli

WORKDIR /usr/src/app
COPY src ./src

# Install requiremnts.txt
RUN pip install -r src/requirements.txt

CMD ["bash"]