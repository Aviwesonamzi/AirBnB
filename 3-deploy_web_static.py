#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers, using the function deploy.

This script calls the do_pack() function to create an archive of web_static,
then deploys the archive to the web servers using the do_deploy(archive_path) function.

Usage:
    Run this script using Fabric with the command:
    fab -f 3-deploy_web_static.py deploy -i <your_ssh_private_key> -u ubuntu

Requirements:
    - Allowed editors: vi, vim, emacs
    - Interpreted/compiled on Ubuntu 20.04 LTS using python3 (version 3.4.0)
    - All files should end with a new line
    - PEP 8 style (version 1.7.*)
    - Fabric 3 version 1.14.post1
    - All files must be executable
    - Documentation for all functions/methods

Example:
    fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
"""

from fabric.api import local, env, run
from fabric.operations import put
from datetime import datetime
import os

# Fabric environment setup
env.user = 'ubuntu'
env.key_filename = '/path/to/your/private/key.pem'
env.hosts = ['3.83.253.101', '54.84.151.192']


def do_pack():
    """
    Creates a compressed archive of web_static folder.

    Returns:
        str: Path to the created archive, or None if archive creation fails
    """
    try:
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        return None


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

        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Delete the uploaded archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents out of extracted folder into main release folder
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the now empty web_static folder
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        current_path = '/data/web_static/current'
        if run('test -L {}'.format(current_path)).failed:
            run('rm {}'.format(current_path))

        # Create a new symbolic link /data/web_static/current linked to the new version
        run('ln -s {} {}'.format(release_path, current_path))

        print('New version deployed!')
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Orchestrates the deployment process by creating and distributing the archive.

    Returns:
        bool: True if deployment is successful, False otherwise
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
