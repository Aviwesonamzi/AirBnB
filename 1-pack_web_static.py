#!/usr/bin/env python3
"""
Fabric script to generate a .tgz archive from web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Creates a .tgz archive from web_static folder.

    Returns:
        Path to the created archive if successful, None otherwise.
    """
    now = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                       now.month,
                                                       now.day,
                                                       now.hour,
                                                       now.minute,
                                                       now.second)
    archive_path = "versions/{}".format(archive_name)

    # Create versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create the .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None
