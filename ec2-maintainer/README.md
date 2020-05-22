# ec2 maintainer

The maintainer removes all data from the day prior and stores it in an AWS S3 bucket called 'inventory-data-repository'. It filters out web crawled data and deletes it. Furthurmore, it delete all of the ip addresses of the users that submitted the data.

### Set up mongodb credentials

Inside of the src directory, create a file called credentials.py that has one line.

`atlas_mondb_endpoint = [ENDPOINT HERE]`

### Install everything

To install all dependencies and set the crontabm, run this command

`sh setup.sh`

Your done! Crontab will execute the maintainer Python script daily at 3 a.m. EST. If there are any issues running the script, the error will be reported in logs.txt
