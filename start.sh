#!/bin/bash
cd ~/daily-lr-files-list-by-user
git pull --all && git submodule update
cd -
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/cleaner.py -pt:0
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/gallery_audio_video.py -pt:0

