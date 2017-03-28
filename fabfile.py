#!/bin/env python

# sudo easy_install fabric

from fabric.api import *

env.hosts = ['tzodih@i-deya.ru']
deploy_path = '/home/djangouser/tzodih/data/otdohni'
touch_file = '/home/djangouser/tzodih/touch'

def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """

    for h in env.hosts:
        try:
            # catch the port number to pass to ssh
            host, port = h.split(':')
            try:
                # catch username too
                user, real_host = host.split('@')
                local('ssh -p %s -A %s -l %s "%s"' % (port, real_host, user, cmd))
            except ValueError:
                local('ssh -p %s -A %s "%s"' % (port, host, cmd))
        except ValueError:
            local('ssh -A %s "%s"' % (h, cmd))

def deploy():
    local('git pull')
    local('git push')

    sshagent_run('cd %s && git pull' % deploy_path)

    with cd(deploy_path):
        run('source .env/bin/activate && pip install -r build/pipreq.txt')
        run('source .env/bin/activate && ./manage.py syncdb')
        run('source .env/bin/activate && ./manage.py migrate --ignore-ghost-migrations')
        run('source .env/bin/activate && ./manage.py compilemessages')
        run('touch %s' % touch_file)

def deploy_lite():
    local('git push')

    sshagent_run('cd %s && git pull' % deploy_path)

    with cd(deploy_path):
        run('source .env/bin/activate && ./manage.py compilemessages')
        run('touch %s' % touch_file)
