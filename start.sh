#!/bin/bash
git pull origin master
python3 cleaner.py -pt:0
python3 main.py -pt:0
