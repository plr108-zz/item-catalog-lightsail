# Udacity Full Stack Web Developer Nanodegree

## Item Catalog Application

By Patrick Roche | [github.com/plr108](https://github.com/plr108) | [patrick.l.roche@gmail.com](mailto:patrick.l.roche@gmail.com)

### Project Overview

This repository contains my submission for the Item Catalog Application project of the [Udacity Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### Installing the Project

1. Download and install [Vagrant](https://www.vagrantup.com/intro/index.html)
2. Download and install [VirtualBox 5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Note: as of October 2017 newer versions of VirtualBox are do not work with the current release of Vagrant.
3. Clone the [Udacity Full Stack Virtual Machine Project](https://github.com/udacity/fullstack-nanodegree-vm) repository.
4. Copy all of the files in this repository into the `vagrant/catalog` folder of the Udacity Full Stack Virtual Machine Project.

### Starting the Project

1. Open console (or Git Bash on a Windows machine) and navigate to the `/vagrant` subdirectory where the project files are installed.
2. Run `vagrant up` to start the virtual machine
3. After the Vagrant virtual machine starts, run `vagrant ssh` to login.
4. Run `cd /vagrant/catalog` to go to the project directory.
5. Run `python database_setup.py` to create the project's PostgreSQL database.
6. Run `python database_populate.py` to add categories to the database.
7. Run `python application.py` to start the Project
8. Navigate to `http://localhost:8000` in your favorite browser to use the project.

### Using the Catalog Application

1. Click the login button to login into the application via Google Sign-In.
2. Signed-In users can create, edit, and delete their own Items.
3. Items can be viewed by anyone.  Click on any Category name to view related Items.
4. Click on any Item to view the item's description.
