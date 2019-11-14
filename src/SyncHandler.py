from git import Repo
import Logger
import os
import distutils.dir_util
import subprocess
import sys

REPO_DIR = ".."

def syncSystem():
    global REPO_DIR
    Logger.info("before git clone - starting new subprocess")
    pullGit()
    Logger.info("starting new subprocess")
    cmd = REPO_DIR + "/start.sh"
    subprocess.run([cmd])
    Logger.info("done new subprocess")

def pullGit():
    global REPO_DIR
    Logger.info("cloning git repo")
    repo = Repo(REPO_DIR).remotes.origin
    repo.pull()
