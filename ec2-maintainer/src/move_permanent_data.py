import pymongo
import boto3
import config

# will run everynight
# will move all data from mongodb to aws s3
# will filter out those with crawler = true

# https://clouductivity.com/amazon-web-services/download-upload-files-amazon-s3-python/
