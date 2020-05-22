# shelfCheck backend

In this repository we have five main folders for different actions
* The lambda functions that controls users actions on the database.
* The ec2 database maintainer that cleans database at night
* The ec2 webscraper of instok that used to work but no longer does
* The ec2 deployment manager that allows builds on servers to automatically redeploy when their origin/master is changed.
* The lambda thawer that allow the lambda functions to stay warm at all time
