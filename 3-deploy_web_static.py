#!/usr/bin/python3
"""
This is a Fabric script (based on the file 2-do_deploy_web_static.py) that
creates and distributes an archive to your web servers
"""

from datetime import datetime
import os
from fabric.api import local, put, run, env
env.hosts = ['161.74.224.1', '']


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


def do_deploy(archive_path):
    """distribute an archive"""
    if not os.path.exists(archive_path):
        return False

    try:
        dest = "/data/web_static/releases/"
        fileName = archive_path.split('/')[-1]
        noExt = archive_path.split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # create folder
        run('mkdir -p {}{}/.format(dest, noExt)')

        # Uncompress the archive to the folder:
        # /data/web_static/releases/<archive filename without extension>
        # on the web server
        run('tar -xzf /tmp/{} -C {}{}/'.format(fileName, dest, noExt))

        # Delete the archive from the web server
        run('rm /tmp/{}.format(fileName)')

        run('mv {0}{1}/web_static/* {0}{1}/'.format(dest, noExt))
        run('rm -rf {}{}/web_static'.format(dest, noExt))

        # Delete the symbolic link /data/web_static/current 4rm the webserver
        run('rm -rf /data/web_static/current')

        # Create a new the symbolic link /data/web_static/current
        # on the web server, linked to the new version of your code:
        # (/data/web_static/releases/<archive filename without extension>)
        run('ln -s {}{}/ /data/web_static/current'.format(dest, noExt))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
