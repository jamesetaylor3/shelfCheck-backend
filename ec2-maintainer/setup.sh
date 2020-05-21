sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install python3.6
sudo apt-get install python3-pip

pip3 install pymongo --user
pip3 install boto3 --user

# crontab the run.py every night at 1:00 AM EST