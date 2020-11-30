FROM python:3.8

ADD /db_reqs.txt db_reqs.txt
RUN pip3.8 install -r /db_reqs.txt

ADD /settings.py settings.py
ADD /prepare_db.py prepare_db.py

CMD ["python3.8", "/prepare_db"]
