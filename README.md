# TICKETING SYSTEM

This system provides a system for event ticketing. It tackles 2 crucial stages of an event: Pre-event and In-event.  

Built using [`random.choice`](https://docs.python.org/3/library/random.html#random.choice) as main engine for random ticket number, along with [qrcode](https://github.com/lincolnloop/python-qrcode) and [python-barcode](https://github.com/WhyNotHugo/python-barcode) for QRcode and Barcode.  

This system also provides a [scanner](bin/scanner.py) and [face recognition]() for checking in/out process.

## Features

These below are main features of the system.

### Seed generated codes

For each unique event, the system can generate unique codes and assign to each unique ID with the number of codes required.


### Scan

Code scanner using [OpenCV]() library to read and preprocess image data. Then [pyzbar]()

### Face recognition



### GoogleSheetAPI

By using API provided by **Google**, it provides data communication between systems. This means this system can be use with **Google Form**. 

This allows:

- Fetching user data from Google Sheet. 
- Updating and Viewing data on Google Sheet.

<!-- ## Demos -->

## Installation

### Requirements

- Python 3.x
- Windows operating system

> *macOs and Linux operating system are under development*



### Installation Options

#### Installing on Windows

Install required packages using Python package controller `pip` by running the following command:

```bash
pip3 install -r requirements.txt
```

> *In case you have any trouble installing **dlib** package for **face_recognition**, please do checkout [@masoudr's Windows 10 installation guide (dlib + face_recognition)](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)*

#### Installing on Mac or Linux

Under Developement.

## Usage

## Deployment to Raspberry Pi

## Having problems?

If you run into problems, please read [Common Errors](https://github.com/fuisl/checkin/wiki/Common-Errors) section on the wifi page before filing a Github issue.

## Acknowledgement

