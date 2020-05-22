import subprocess
import time
from redeploy import redeploy

WAITING = 60

def hasChanged():
	return len(subprocess.check_output(['git', 'diff', 'origin/master'])) != 0


if __name__ == '__main__':
	while True:
		if hasChanged():
			redeploy()
		time.sleep(WAITING)