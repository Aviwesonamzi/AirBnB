#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
import os

env.hosts = ['3.83.253.101', 'IP 54.84.151.192']

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/{}".format(archive_file[:-4])

        put(archive_path, "/tmp/{}".format(archive_file))
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_file, archive_folder))
        run("rm /tmp/{}".format(archive_file))
        run("mv {}/web_static/* {}/".format(archive_folder, archive_folder))
        run("rm -rf {}/web_static".format(archive_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(archive_folder))
        return True
    except:
        return False
