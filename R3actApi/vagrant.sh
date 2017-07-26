#!/usr/bin/env bash

# Upgrade apt-get first
sudo apt-get update

# Install Python pip with --yes as the default argument
sudo apt-get install python-pip --yes

# Install virtualenv used for 485 projects
sudo pip install virtualenv

# By default, while installing MySQL, there will be a blocking prompt asking you to enter the password
# Next two lines set the default password of root so there is no prompt during installation
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'

# Install MySQL server with the default argument --yes
sudo apt-get install mysql-server --yes
sudo apt-get install build-essential python-dev libmysqlclient-dev --yes
sudo apt-get install gcc --yes

# Go to working directory
# This folder is synced on the VM with your local directory where the Vagrantfile is
cd /vagrant
rm -rf venv

# Set up a virtual environment in the current working directory
virtualenv venv --distribute --always-copy

# Use the virtual environment as the terminal shell
source venv/bin/activate

# Install the project requirements given in the requirements.txt file in your working directory
pip install -r requirements.txt
