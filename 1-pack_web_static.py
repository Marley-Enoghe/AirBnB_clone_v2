#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack
"""

from datetime import datetime
import os
from fabric.api import local


def do_pack():
    """creates a .tgz file"""
    try:
        if not os.path.exists("versions") and not os.path.isdir("versions"):
            local("mkdir versions")
        formatted_date = datetime.now().strftime('%Y%m%d%H%M%S')
        fileName = "versions/web_static_{}.tgz".format(formatted_date)
        local("tar -cvzf {} web_static".format(fileName))
        return fileName
    except:
        return None
