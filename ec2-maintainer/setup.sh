yum install python36
alternatives --set python /usr/bin/python3.6

cd /tmp/
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip3 --version


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