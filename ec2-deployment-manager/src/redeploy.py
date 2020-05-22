import subprocess

REPO_PATH = "~/Documents/shelfCheck/shelfCheck-backend"

RESET = ['git', 'reset', '--hard', 'HEAD']
CLONE = ['git', 'clone', '--force']
BUILD = ['sudo', 'npm', 'run', 'build']
LIST_PROCESSES = ['ps', 'xw']
KILL = ['kill', '-9', '']
SERVE = ['nohup', 'serve', '-s', 'build', '&']

def RUN(action):
	return subprocess.check_output(action, cwd=repo_path)

def redeploy():
	RUN(RESET)
	RUN(CLONE)
	RUN(BUILD)
	out = RUN(LIST_PROCESSES)

	processes = out.split('\n')

	for p in processes:
		if 'serve -s build' in p:
			pid = p.split()[0]
			KILL[2] = pid

	RUN(KILL)

	RUN(SERVE)
