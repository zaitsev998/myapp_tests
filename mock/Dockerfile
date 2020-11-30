FROM python:3.8

ADD /code code
RUN pip3.8 install -r /code/mock_reqs.txt

CMD ["python3.8", "/code/vk_api.py"]
