FROM python:3
RUN mkdir /opt/compromised-account-detector
WORKDIR /opt/compromised-account-detector
ADD . /opt/compromised-account-detector
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
EXPOSE 5000
CMD [ "python", "app.py" ]
