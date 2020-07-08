#!/bin/bash
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/cleaner.py -pt:0 -dir:~/daily-lr-files-list-by-user
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/gallery.py -pt:0 -dir:~/daily-lr-files-list-by-user
~/lr-list-env/bin/python3 ~/daily-lr-files-list-by-user/sorted_list.py -pt:0 -dir:~/daily-lr-files-list-by-user
