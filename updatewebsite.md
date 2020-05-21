# How to update the website

### SSH into EC2 instance

Using the terminal, ssh into the the ubuntu user of the EC2 instance with attached private key

`$ ssh -i ~/path/to/shelfcheck.pem ubuntu@ec2-3-92-2-15.compute-1.amazonaws.com`

### Download and build new package

This step pulls the most recent repository from github and builds with production optimized

```
$ cd ~/ShelfCheck-Website/

$ git pull --force

$ sudo npm run build

```

### Find and stop current instance from running

Type in this command to get a list of current processes

`$ ps xw`

You will receive an output that looks similar to this. Find the PID of the process that is running command `serve -s build`. In this case it is 2009

```
  PID TTY      STAT   TIME COMMAND
 1186 ?        Ss     0:00 /lib/systemd/systemd --user
 1197 ?        S      0:00 (sd-pam)
 2009 ?        Sl     0:01 /snap/node/2310/bin/node /usr/local/bin/serve -s build
 2425 ?        S      0:00 sshd: ubuntu@pts/0
 2426 pts/0    Ss     0:00 -bash
 2787 pts/0    R+     0:00 ps xw

```

To kill the process, type this command where PID is the PID of the process you want to kill

`kill -9 PID`

More specifically to the example above

`kill -9 2009`

### Start the new instance

To keep the instance running when we exit the shell, we are going to use something called `nohup`. Run the following command from within the ShelfCheck-Website directory.

`nohup serve -s build &`

After this step, you are done and the new update should be running!
