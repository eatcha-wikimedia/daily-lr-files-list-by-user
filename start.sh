#!/bin/bash
cd ~/daily-lr-files-list-by-user
git pull --all && git submodule update
cd -
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/cleaner.py -pt:0 -dir:/data/project/eatchabot/daily-lr-files-list-by-user
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/gallery_audio_video.py -pt:0 -dir:/data/project/eatchabot/daily-lr-files-list-by-user
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/gallery_image.py -pt:0 -dir:/data/project/eatchabot/daily-lr-files-list-by-user
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/sorted_list.py -pt:0 -dir:/data/project/eatchabot/daily-lr-files-list-by-user
