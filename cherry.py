# (RUN like this) python3 arg1 arg2 arg3

#(example) python3 cherry.py d develop/dev-child_branch t

# arg1 : b/d ----> which folder ? backend or database
# arg2 : develop/dev-{child_branch} ------> name child_branch using _ (underscore) but never with  - (hyphen)
# arg3 : t/u/m ------> which env ? test/uat/main

import sys
import os
import subprocess

def get_commits_to_cherry_pick(child_branch):

    try:
        cmd = f"git cherry -v develop/dev {child_branch}" # this will give our recent new commits in child branch
        result = subprocess.check_output(cmd, shell=True, text=True)
    except:
        print("no such child branch exist")
        exit()
    
    commits = result.strip().split("\n")
    return [commit.split()[1] for commit in commits]

def cherry_pick_commits(commits,env,child_branch):

    os.system(f'git checkout {env}' )
    os.system('git pull')
    os.system(f"git checkout -b {env}-{child_branch}" )
    
    for commit_hash in commits:

        cmd = f"git cherry-pick {commit_hash}"
        try:
            subprocess.check_call(cmd, shell=True)
            print(f"----------------------- Cherry-picked commit: {commit_hash} ---------------------------")
        except subprocess.CalledProcessError:
            print(f"Cherry-pick failed for commit: {commit_hash}")

    os.system("git branch --show-current | xargs -I{} git push --set-upstream origin  {}") # git push
    exit()

if __name__ == "__main__":

    arg1 = sys.argv[1]

    if arg1 == 'b':
        folder = "/Users/kailashkangne/Desktop/ia/mtp-inventorysmart-backend"
    elif arg1=='d':
        folder = "/Users/kailashkangne/Desktop/inv Smart/mtp-database"
    else:
        print(f"no folder exist like arg1 = {arg1}")
        exit()

    try:
        os.chdir(folder)
    except:
        print("can't able to change directory")
        exit()
    
    child_branch = sys.argv[2]
    env = sys.argv[3]

    branch = {
        'u':'develop/uat',
        'm':'main',
        't':'develop/test'
    }
    
    if env := branch[f'{env}'] :

        commits_to_cherry_pick = get_commits_to_cherry_pick(child_branch)

        child_branch = child_branch.split('-')[1]

        cherry_pick_commits(commits_to_cherry_pick,env,child_branch)

    else:
        print("wrong ENV")
        exit()