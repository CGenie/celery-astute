packages:
  pkg.latest:
    - names:
      - python-pip
      - rabbitmq-server
      - tmux

python-requirements:
  cmd.run:
    - name: pip install -r /vagrant/requirements.txt
    - require:
      - pkg: packages

/usr/bin/attach-tmux.sh:
  file.managed:
    - source: salt://packages/attach-tmux.sh
    - mode: 755
