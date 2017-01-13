#1 usr/bin/bash

# Alex Geoffrey
# apg@uoregon.edu
# CIS 322 Software Engineering
# Assignment 1

# Clone postgres source code
git clone https://github.com/postgres/postgres.git

# Configure, make and install postgres
postgres/configure --prefix="$HOME/installed"
make
make install

# Download compressed file into tar.bz2 file
curl http://apache.spinellicreations.com//httpd/httpd-2.4.25.tar.bz2 >> httpd-2.4.25.tar.bz2

# Unpack tar file and change directory
tar xvf httpd-2.4.25.tar.bz2
cd httpd-2.4.25

# Configure, make and install httpd
./configure --prefix="$HOME/installed"
make
make install

# Optional, to change port listener to port 8080
# nano $HOME/installed/conf/httpd.conf
