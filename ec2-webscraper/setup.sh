sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install python3.6
sudo apt-get install python3-pip


pip3 install boto3 --user
pip3 install pymongo --user
pip3 install selenium --user

cd /tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
chromedriver --version

curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version && which google-

# need to have crontab run 
