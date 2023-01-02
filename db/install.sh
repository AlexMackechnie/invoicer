#!/bin/bash

# Update
sudo apt update
sudo apt install sqlite3

# Create dir for the DB
sudo mkdir /db

sqlite3 /db/invoicer.db < commands.sql

