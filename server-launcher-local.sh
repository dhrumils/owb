#!/bin/bash

# Kill server and run again
ps aux | grep 'python server_launcher.py' | awk '{print $2}' | sudo xargs kill -9
ps aux | grep 'server_launcher.py' | awk '{print $2}' | sudo xargs kill -9
sudo python server_launcher.py
