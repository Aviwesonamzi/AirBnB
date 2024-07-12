#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives.
"""

from fabric.api import *
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '<path_to_ssh_key>'

def do_clean(number=0):
    """Delete out-of-date archives."""
    number = int(number)

    if number == 0:
        number = 1

    # Local cleanup
    local_archives = sorted(os.listdir("versions"))
    [local_archives.pop() for _ in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in local_archives]

    # Remote cleanup
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        [remote_archives.pop() for _ in range(number)]
        [run("rm -rf ./{}".format(a)) for a in remote_archives]
