# TICKETING SYSTEM

This system provides a system for event ticketing. It tackles 2 crucial stages of an event: Pre-event and In-event.  

Built using [`random.choice`](https://docs.python.org/3/library/random.html#random.choice) as main engine for random ticket number, along with [qrcode](https://github.com/lincolnloop/python-qrcode) and [python-barcode](https://github.com/WhyNotHugo/python-barcode) for QRcode and Barcode.  

This system also provides a [scanner](bin/scanner.py) and [face recognition]() for checking in/out process.

## Features

The Tickting System offers the following key features:

### Seed generated codes

For each unique event, the system can generate a set of unique codes and assign them to individual attendees.

### Scan

The system includes a code scanner that utilizes the **OpenCV** library for reading and preprocessing image data. It also incorporates the **pyzbar** library for code decoding.

### Face recognition

> *This feature is currently under development and will be available in future updates.*

### GoogleSheetAPI

The system leverages the GoogleSheetAPI to facilitate data communication between systems. It allows for fetching user data from Google Sheets, as well as updating and viewing data within the sheets. This integration enables the use of Google Forms with the Tickting System.

## Installation

### Requirements

- Python 3.x
- Windows operating system *(macOS and Linux versions are currently in development)*

### Installation Options

#### Windows

To install the required packages, use the Python package controller `pip` and run the following command:

```bash
pip3 install -r requirements.txt
```

If you encounter any issues while installing the `dlib` package for `face_recognition`, refer to [@masoudr's Windows 10 installation guide (dlib + face_recognition)](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508) for troubleshooting steps.

#### macOS and Linux

These installation instructions are currently under development.

## Usage

Usage instructions will be provided in future updates.

## Deployment to Raspberry Pi

Instructions for deploying the Tickting System to a Raspberry Pi will be provided in future updates.

## Troubleshooting

If you encounter any problems, please refer to the [Common Errors](https://github.com/fuisl/checkin/wiki/Common-Errors) section on the wiki page before submitting a GitHub issue.

## Acknowledgement