import os
import sys
import subprocess
import confidential
import atexit
import json
from subprocess import DEVNULL, STDOUT
from bottle import post, run, request

fn_name = sys.argv[1]

if not os.path.isdir(f'src/{fn_name}'):
	print('not valid function name')
	sys.exit()

def exit_handler():
	# clean up
	print('cleaning up...')
	subprocess.check_call(['rm', '-r', target_path])
	subprocess.check_call(['rm', '-r', '__pycache__'])

	print('finished!')

atexit.register(exit_handler)

src_path = os.path.join('src', fn_name)
target_path = f'{fn_name.replace("-", "_")}_target'

src_handler_path = os.path.join(src_path, 'handler.py')

target_handler_path = os.path.join(target_path, 'lambda_function.py')

print('creating target folder...')
subprocess.check_call(['mkdir', target_path])
subprocess.check_call(['cp', src_handler_path, target_handler_path])
subprocess.check_call(['touch', '__init__.py'], cwd=target_path)

print()

exec(f'import {target_path}.lambda_function as lf')

@post(f'/')
def index():
	event = {'body': json.dumps(request.json)}
	context = None
	return json.loads(lf.lambda_handler(event, context)['body'])

run(host='localhost', port=8080)