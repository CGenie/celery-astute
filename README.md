Celery-Astute
=============

Showoff of Celery's chaining/grouping capabilities that could be used as the
base for making an orchestration system.

Usage:

```
vagrant up
vagrant ssh
sudo salt-call state.highstate
attach-tmux.sh
from proj import tasks
r = tasks.deploy()
rr = r.delay()
rr.get()
```
