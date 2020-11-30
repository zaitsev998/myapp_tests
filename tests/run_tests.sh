#!/bin/bash

rm -rf /alluredir/*
pip3.8 install -r /myapp_tests/tests/test_reqs.txt
pytest -s -l -v /myapp_tests --alluredir=/alluredir