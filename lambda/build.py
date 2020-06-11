import os
import sys
import subprocess
import confidential
from subprocess import DEVNULL, STDOUT

fn_name = sys.argv[1]

if not os.path.isdir(f'src/{fn_name}'):
	print('not valid function name')
	sys.exit()

src_path = os.path.join('src', fn_name)
target_path = f'{fn_name}-target'

src_handler_path = os.path.join(src_path, 'handler.py')
config_path = os.path.join(src_path, 'config.py')

target_handler_path = os.path.join(target_path, 'lambda_function.py')

print('creating target folder...')
subprocess.check_call(['mkdir', target_path])
subprocess.check_call(['cp', src_handler_path, target_handler_path])
subprocess.check_call(['cp', config_path, '.'])

# this is the functions config file
import config

print('installing pip dependencies...')

# figure out why installing dist info or remove it
for dep in config.pip_dependencies:
	print(f' -> {dep}')
	subprocess.check_call(['pip3', 'install', dep, '-t', '.'], stdout=DEVNULL, stderr=STDOUT, cwd=target_path)

# add the confidential stuff
if len(config.confidential_dependencies) != 0:

	print('including confidential dependencies...')
	confidential_path = os.path.join(target_path, 'confidential.py')

	confidential_file = open(confidential_path, 'a')

	for dep in config.confidential_dependencies:
		if dep == 'mongo':
			print(f' -> mongo')
			confidential_file.write(f'MONGO = \'{confidential.MONGO}\'\n')

		if dep == 'aws':
			print(f' -> aws')
			confidential_file.write(f'AWS = \'{confidential.AWS}\'\n')

		if dep == 'mapbox':
			print(f' -> mapbox')
			confidential_file.write(f'MAPBOX = \'{confidential.MAPBOX}\'\n')

	confidential_file.close()


# add the shelfcheck dependencies
print('including the shelfcheck dependencies...')

for dep in config.shelfcheck_dependencies:
	if dep == 'prop':
		print(f' -> prop')
		prop_target_path = os.path.join(target_path, 'prop.py')
		subprocess.check_call(['cp', 'src/prop.py', prop_target_path])

	if dep == 'shopper':
		print(f' -> shopper')
		shopper_target_path = os.path.join(target_path, 'shopper.so')
		subprocess.check_call(['cp', 'src/shopper.so', shopper_target_path])

# zip it
print('zipping the target...')
target_zip = f'../{target_path}.zip'
subprocess.check_call(['zip', '-r', target_zip, '.'], stdout=DEVNULL, stderr=STDOUT, cwd=target_path)

# clean up
print('cleaning up directory...')
subprocess.check_call(['rm', 'config.py'])
subprocess.check_call(['rm', '-r', target_path])
subprocess.check_call(['rm', '-r', '__pycache__'])

print('finished!')