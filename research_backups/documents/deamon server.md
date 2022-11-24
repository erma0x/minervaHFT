# IMPORTANT commands for server

### lunch deamon
```ssh -o ServerAliveInterval=5 -o ServerAliveCountMax=2 $HOSTNAME```
```sudo nohup python3 teleryum.py > /path/to/custom.out &```

### find process id
```ps aux | grep teleryum.py```

### kill deamon
```kill -9 <processID>```

# Other commands for server

### Start deamons with nohup

```nohup python3 teleryum.py > /path/to/custom.out &```

```nohup ./mn.sh > myscipt.sh &```

### get process id

```ps aux | grep teleryum.py```

```pgrep -a teleryum.py```


### kill processes

```kill -9 <PID>```

```kill -l```

```kill <PID>```


There are many fiddly things to take care of when becoming a well-behaved daemon process:

- prevent core dumps (many daemons run as root, and core dumps can contain sensitive information)

- behave correctly inside a chroot gaol

- set UID, GID, working directory, umask, and other process parameters appropriately for the use case

- relinquish elevated suid, sgid privileges

- close all open file descriptors, with exclusions depending on the use case

- behave correctly if started inside an already-detached context, such as init, inetd, etc.

- set up signal handlers for sensible daemon behaviour, but also with specific handlers determined by the use case

- redirect the standard streams stdin, stdout, stderr since a daemon process no longer has a controlling terminal

- handle a PID file as a cooperative advisory lock, which is a whole can of worms in itself with many contradictory but valid ways to behave

- allow proper cleanup when the process is terminated

- actually become a daemon process without leading to zombies
