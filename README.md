# Water Meter Monitor
This repository contains 3 files.
This project is a water detection system (using Raspberry Pi Zero 2 W and Raspberry Pi camera module) to identify water usage in residential units over time


## The Problem

Water bills increased significantly after a new tenant moved in. Needed a way to track consumption patterns and potentially identify abnormal usage.


## The Hardware

- Raspberry Pi Zero 2 W
- Raspberry Pi Camera Module
- MicroSD Card
- Power supply

## Hardware Setup

1. Insert MicroSD Card into Raspberry Pi Zero 2 W
2. Attach and connect Raspberry Pi Camera Module
3. Plug in HDMI adapter Monitor Cord
4. Plug in USB Dongle for wireless mouse and keyboard
5. Plug in Power Cord to turn on Raspberry Pi Zero 2 W


## Software Setup

1. Install Operating System (OS)
2. Set up Raspberry Pi account and password
3. Create Public/Private Key


## Files

timelapse.py - this python script takes a picture every 30 minutes and saves it to the SD card
copy_pics.ps1 - this powershell script copies the images taken since the previous download to a laptop
read_meters_Claude.py - this Python script optically reads the analog water meter and puts the entry into a Google Sheet


