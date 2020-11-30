FROM python:3.8

ADD /mock_reqs.txt mock_reqs.txt
RUN pip3.8 install -r /mock_reqs.txt

ADD /settings.py settings.py
ADD /vk_api.py vk_api.py

CMD ["python3.8", "/vk_api.py"]
