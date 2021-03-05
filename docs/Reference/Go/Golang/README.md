Download and install
1. Go download.
2. Go install.
3. Go code.

Download and install Go quickly with the steps described here.

For other content on installing, you might be interested in:

Managing Go installations -- How to install multiple versions and uninstall.
Installing Go from source -- How to check out the sources, build them on your own machine, and run them.
1. Go download.
Click the button below to download the Go installer.

Download Go
Visit the downloads page.
Don't see your operating system here? Try one of the other downloads.

Note: By default, the go command downloads and authenticates modules using the Go module mirror and Go checksum database run by Google. Learn more.
2. Go install.
Select the tab for your computer's operating system below, then follow its installation instructions.

Linux Mac Windows
If you have a previous version of Go installed, be sure to remove it before installing another.

Download the archive and extract it into /usr/local, creating a Go tree in /usr/local/go.
For example, run the following as root or through sudo:

tar -C /usr/local -xzf go1.14.3.linux-amd64.tar.gz
Add /usr/local/go/bin to the PATH environment variable.
You can do this by adding the following line to your $HOME/.profile or /etc/profile (for a system-wide installation):

export PATH=$PATH:/usr/local/go/bin
Note: Changes made to a profile file may not apply until the next time you log into your computer. To apply the changes immediately, just run the shell commands directly or execute them from the profile using a command such as source $HOME/.profile.

Verify that you've installed Go by opening a command prompt and typing the following command:
$ go version
Confirm that the command prints the installed version of Go.
3. Go code.
You're set up! Visit the Getting Started tutorial to write some simple Go code. It takes about 10 minutes to complete.
