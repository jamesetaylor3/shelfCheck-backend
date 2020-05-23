import subprocess
import time
from redeploy import redeploy

WAITING = 5

REPO_PATH = "../../../ShelfCheck-Website"

def hasChanged():
	subprocess.check_output(['git', 'fetch', 'origin', 'master'], cwd=REPO_PATH)
	return len(subprocess.check_output(['git', 'diff', 'origin/master'], cwd=REPO_PATH)) != 0


if __name__ == '__main__':
	while True:
		if hasChanged():
			redeploy()
		time.sleep(WAITING)
