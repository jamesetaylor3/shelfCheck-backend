sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3.6

nohup sh src/listen.sh & > logs.txt 2>&1

echo "Done setting up!"
