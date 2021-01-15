General
---

This container is a general-purpose ubuntu container to use as a pwning setup, with some nice additions to make working on problems more seamless.

Some nice defaults:
- Your host user is made a guest user in the container
- terminal fonts, colors, and a default shell prompt already set up
- some useful programs for ctfs are already added to the container
- gdb w/ gef is preinstalled (comment out the line installing gef in the config if you prefer a different gdb extension)
- your entire user system (/home/USER) is mounted within the container at the same location, so you can easily access any of your host user's files
- port 9998 and 9999 are forwarded to/from the host if you want to use socat and gdbserver

Prereqs
----
You must have a working installation of docker on your machine.

Usage
----

Just run `./start-container` and the container will build and run. Subsequent runs will only run the container unless the Dockerfile is modified.

If you want to make changes to the docker container (adding more applications) make sure not to modify existing installation commands or else you'll need to rebuild your entire docker container each time.


All credit goes to Robert Xiao, who shared this config with me. I've only added some small niceties on top and made the config more generic so it requires less setup.


