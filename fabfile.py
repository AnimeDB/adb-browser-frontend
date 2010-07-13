from fabric.api import env, local, run
from fabric.contrib.project import rsync_project
import os
from datetime import datetime

def css():
    """
    Rebuilds all css files from scratch.
    """
    local("(cd assets/sass ; compass)")