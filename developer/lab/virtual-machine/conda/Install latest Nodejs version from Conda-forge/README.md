Install Nodejs latest version from Conda-forge

By default, conda will install nodejs, npm and other required packages from the default channel. 
The packages in the default channel are maintained by the conda team from Anaconda, Inc. 
They are stable, well-tested, but mostly out-dated. 

If you want newer version of packages, install them from Conda-forge channel. 
The conda-forge channel is a community maintained repository that provides conda packages for a wide range of software.

As you may noticed, the version of node installed from default channel is 10.13.0. 
The Conda-forge channel has recent version of node, so we can install latest nodejs version from this channel.

First, delete the old environments as shown in the Remove conda environments section.

Then, run the following command to create a new environment called "nodeenv" and install latest nodejs version from conda-forge channel:

$ conda create -c conda-forge -n nodeenv nodejs



Activate the nodeenv environment:

$ conda activate nodeenv



Check the node version:

$ node --version



v15.3.0
Please note that npm version may not be always up-to-date. To update it, simply run:

$ npm install -g npm@latest


Check npm version:

$ npm --version



7.5.4
That's it. In this guide, you learned how to create virtual environments for Nodejs programs using conda package manager. 
You also learned how to install latest Nodejs version from Conda-forge repository. If you are a developer, 
you can make use of Anaconda to create multiple virtual environments for testing your JavaScript applications.
