import subprocess

REPO_PATH = "../../../ShelfCheck-Website"

RESET = ['git', 'reset', '--hard', 'HEAD']
CLONE = ['git', 'pull', '--force']
BUILD = ['sudo', 'npm', 'run', 'build']


def RUN(action):
	return subprocess.check_output(action, cwd=REPO_PATH)

def redeploy():
	print("updating")
	RUN(RESET)
	RUN(CLONE)
	RUN(BUILD)
