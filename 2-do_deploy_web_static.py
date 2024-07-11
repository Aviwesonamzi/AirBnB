#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers and deploys it.

This script uploads a specified archive to the /tmp/ directory of the web server,
uncompresses the archive to the folder /data/web_static/releases/<archive filename without extension>,
deletes the archive from the web server, deletes the symbolic link /data/web_static/current,
and creates a new symbolic link /data/web_static/current linked to the new version of your code.

Usage:
    Run this script using Fabric with the command:
    fab -f 2-do_deploy_web_static.py do_deploy:archive_path=<archive_path>

    Replace <archive_path> with the path to the .tgz archive to deploy.

Requirements:
    - Allowed editors: vi, vim, emacs
    - Interpreted/compiled on Ubuntu 20.04 LTS using python3 (version 3.4.0)
    - All files should end with a new line
    - PEP 8 style (version 1.7.*)
    - Fabric 3 version 1.14.post1
    - All files must be executable
    - Documentation for all functions/methods

Example:
    fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static_20170315003959.tgz
"""

from fabric.api import env, put, run, sudo
from os.path import exists
from datetime import datetime
import os

# Fabric environment setup
env.user = 'ubuntu'
env.key_filename = ['/path/to/your/private/key.pem']
env.hosts = ['3.83.253.101', '54.84.151.192']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    Args:
        archive_path (str): Path to the archive to deploy

    Returns:
        bool: True if all operations were successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>/
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]
        release_path = '/data/web_static/releases/{}'.format(archive_no_ext)

        sudo('mkdir -p {}'.format(release_path))
        sudo('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Delete the uploaded archive from the web server
        sudo('rm /tmp/{}'.format(archive_filename))

        # Move contents out of extracted folder into main release folder
        sudo('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the now empty web_static folder
        sudo('rm -rf {}/web_static'.format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        current_path = '/data/web_static/current'
        if exists(current_path):
            sudo('rm {}'.format(current_path))

        # Create a new symbolic link /data/web_static/current linked to the new version
        sudo('ln -s {} {}'.format(release_path, current_path))

        print('New version deployed!')
        return True

    except Exception as e:
        print(e)
        return False
