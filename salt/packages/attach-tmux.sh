#!/bin/bash

cd /vagrant

tmux new-session -s 'salt' -d 'celery -A proj worker -l info'
tmux new-window 'ipython'

tmux attach-session -t 'salt'
