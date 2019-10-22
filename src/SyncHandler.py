from git import Repo
import ConfigHandler
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
    #returned_value = os.system(cmd)
    ##Logger.info("returned_value: " + str(returned_value))
   

def pullGit():
    global REPO_DIR
    Logger.info("cloning git repo")
    #Repo(REPO_DIR)
    #distutils.dir_util.remove_tree(CLONED_REPO_DIR)
    #Repo.pull_from(ConfigHandler.getGitRepo(), CLONED_REPO_DIR+ "/")
    #distutils.dir_util.copy_tree(CLONED_REPO_DIR, "../")