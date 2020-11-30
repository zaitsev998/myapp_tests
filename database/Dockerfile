FROM python:3.8

ADD /code code
RUN pip3.8 install -r /code/db_reqs.txt

CMD ["python3.8", "/code/prepare_db.py"]
