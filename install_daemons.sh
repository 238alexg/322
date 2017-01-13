#1 usr/bin/bash

# Alex Geoffrey
# apg@uoregon.edu
# CIS 322 Software Engineering
# Assignment 1

# Clone postgres source code
git clone https://github.com/postgres/postgres.git

# Configure, make and install postgres
./configure --prefix="$HOME/installed"
make
make install

# Download compressed file
curl http://apache.spinellicreations.com//httpd/httpd-2.4.25.tar.bz2

# Configure, make and install httpd
./configure --prefix="$HOME/installed"
make
make install