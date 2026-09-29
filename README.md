This repository contains 3 files.
This project is a water detection system (using Raspberry Pi Zero 2 W and Raspberry Pi camera module) to identify water usage in residential units over time


1. The Problem

Problem: Water bills increased significantly after a new tenant moved in. Needed a way to track consumption patterns and potentially identify abnormal usage.



2. The Hardware Setup

- Raspberry Pi Zero 2 W
- Raspberry Pi Camera Module
- MicroSD Card
- Power supply

Insert MicroSD Card into Raspberry Pi Zero 2 W
Attach and connect Raspberry Pi Camera Module
Plug in HDMI adapter Monitor Cord
Plug in USB Dongle for wireless mouse and keyboard
Plug in Power Cord to turn on Raspberry Pi Zero 2 W



3. Development Process

Setup
Install Operating System (OS)
Set up Raspberry Pi account and password
Create Public/Private Key



4. Coding Implementation

timelapse.py - this python script takes a picture every 30 minutes and saves it to the SD card
copy_pics.ps1 - this powershell script copies the images taken since the previous download to a laptop
read_meters_Claude.py - this Python script optically reads the analog water meter and puts the entry into a Google Sheet


