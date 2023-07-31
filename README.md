# TICKETING SYSTEM

Introduction

## Features

The ticketing system encompasses the following key features:

### Code Generation and Rendering

The system generates unique codes and renders them into QR codes or barcodes upon ticket purchase. These codes serve as secure digital representations of tickets and contain essential information for verification.

### Code Check-in

The system offers a Code Scanner module that enables efficient check-in using QR code and barcode scanning. Event attendees present their codes, and the system instantly validates them, granting access only to valid ticket holders.

### Face Recognition Check-in

The ticketing system incorporates a FaceScanner module that utilizes face recognition technology. Attendees' faces are detected, and their identities are matched with the registered attendees' database to facilitate seamless check-in.

### Web-based Ticket/User Management

The system provides a web-based interface where event organizers can efficiently manage and record ticket and user information. This web application allows organizers to view attendee data, track attendance, and perform essential administrative tasks.

### AdafruitIO Dashboard Monitorin

The ticketing system integrates with AdafruitIO Dashboard, creating an admin dashboard that displays the current status of the running system. Event organizers can monitor real-time data and gain valuable insights into attendee demographics and check-in patterns.

## Deployment

### Requirements

- Python 3.x
- CPU (optionally with GPU) that are capable of running all the required libraries/dependencies.
- MongoDB (optionally with MongoDBCompass)
- AdafruitIO Account

### Installation

1. Clone this repository

    ```bash
    git clone https://github.com/fuisl/checkin.git
    ```

2. Install the required packages

    To install the required packages, use the Python package controller `pip` and run the following command:

    ```bash
    pip3 install -r requirements.txt
    ```

    > If you encounter any issues while installing the `dlib` package for `face_recognition`, refer to [@masoudr's Windows 10 installation guide (dlib + face_recognition)](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508) for troubleshooting steps.  

    > *In case you have CUDA compatable device, you can build `dlib` with GPU support. This makes the training and detecting process much faster. Follow these steps to proceed install dlib with GPU*  

    <details>
    <summary markdown="span">Install dlib with GPU (optional)</summary>

    1. Clone the repository from @davisking

        ```bash
        git clone https://github.com/davisking/dlib.git
        ```

    2. Create a build folder inside dlib

        ```bash
        cd dlib
        mkdir build
        cd build
        ```

    3. Run cmake

        ```bash
        cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
        cmake --build .
        ```

    4. Run `setup.py`

        ```bash
        cd ..
        python setup.py install --yes USE_AVX_INSTRUCTIONS --yes DLIB_USE_CUDA
        ```

    </details>

### Initialize Database

For this step, it is best to use MongoDB Compass to intialize database and establish connection:

1. Connect to datase using MongoDB

    Enter the following URL to connect:

    ```bash
    mongodb://localhost:27017
    ```

    ![MongoDB-Connection](https://github.com/fuisl/checkin/assets/135719107/1f8d33d5-ef33-4d9f-9694-6cb98928f460)

2. Create a new database by clicking plus sign. Create database with name `web_db` and a collection `user` if prompted.

    ![create-database](https://github.com/fuisl/checkin/assets/135719107/00409ab8-d3e6-4bc1-b08e-7b2c22041775)

> *Since MongoDB automatically creates collection if the collection doesn't exist, there is no need for creating all the collection by yourself.*

### Create AdafruitIO Feed and Dashboard

#### Create Feeds

The feed is used to store the data from the system. The system uses 5 feeds as in the picture below:

![AdafruitIO-Feeds](https://github.com/fuisl/checkin/assets/135719107/a27784c6-523f-4a49-96ee-09c6db8738d8)

- continue: This feed is used to send continue signal to the system. The system will continue to run (paused = False) if a button is pressed on the dashboard.
- face: This feed is used to display frame with face detection on the dashboard.
- info: This feed is used to display user information on the dashboard.
- pause: This feed is used to send pause signal to the system. This feed is used for switching pause and continue signal.
- traffic: This feed is used to display people/minute (aka. traffic) information on the dashboard.

#### Create Dashboard

The recommended dashboard layout is shown below:

![dashboard-layout](https://github.com/fuisl/checkin/assets/135719107/99222e2a-f4d4-4ff9-97d6-52bd17fbfa30)

This contains 5 blocks that goes along with the feeds created above.

### Deployment to Raspberry Pi

Instructions for deploying the Tickting System to a Raspberry Pi will be provided in future updates. 

## Usage

*The instruction provided below are for the implementation of the whole system, that is follows an order. If you want to use only a part of the system, be sure to understand the dependencies of each module.*

### Generate Codes and Rendering

- `Gen()` class takes 1 optional argument: event_code. If no argument is provided, the default event_code is `default`.

- `gen(ticket_info)` method takes 1 argument: ticket_info. This argument is a dictionary that specify the classes and quantity of the class.

    ```python
    ticket_info = {
        'class1': 10,
        'class2': 20,
        'class3': 30
        }
    ```

- `encode()` method takes 3 optional arguments (normally, for this framework, you woudn't need to use arguments), and update the code list in database.

    ```python
    encode(type='qr', ticket_info=ticket_info, transparent=True)
    ```

    This method also provides transparent argument to make the rendered code transparent. This is useful when you want to print the QR code on a ticket.

### Host Web Application for importing data

- `app.py` is the main file for hosting the web application. Run the following command to start the web application:

    ```bash
    python3 app.py
    ```

- The web application is hosted on `localhost:5000` by default. You can access the web application by entering the following URL in your browser:

    ```bash
    http://localhost:5000
    ```

- The web application provides the following functionalities:

  - Register new users and tickets to the database.
  - View existing users and tickets in the database.
  - Import face images for face recognition *(only if number of tickets equals 1)*.

### Train Face Recognition Model

- `train.py` is the main file for training the face recognition model. Run the following command to start the training process:

    ```bash
    python3 train.py <train_dir> <model_save_path>
    ```

    > *The value for `train_dir` should be specified, and `model_save_path` must include `.clf` extention.*  
    > E.g. `./models/trained_knn_model.clf`.

### Check-in using Scanner

Implementing the check-in process using the scanner module requires the following steps:

#### Face Scanner

1. Import the `FaceScanner` from `scanner.py`:

    ```python
    from scanner import FaceScanner
    ```

2. Initialize the `FaceScanner` class and setup AdafruitIO credentials:

    ```python
    face_scanner = FaceScanner()
    
    adafruit_account = {"username":"fuisl",
                        "key":"..."}
    face_scanner.set_ada_info(adafruit_account)
    ```

3. Load the face recognition model with the `load_model()` method of the `FaceScanner` class:

    ```python
    face_scanner.load_model(model_path='./models/trained_knn_model.clf')
    ```

3. Connect to a camera with the `connect()` method of the `FaceScanner` and `CodeScanner` class:

    ```python
    face_scanner.connect()
    ```

4. Run the `scan()` method of the `FaceScanner` and `CodeScanner` class:

    ```python
    face_scanner.scan()
    ```

#### Code Scanner

1. Import the `CodeScanner` from `scanner.py`:

    ```python
    from scanner import CodeScanner
    ```

2. Initialize the `CodeScanner` class and setup AdafruitIO credentials:

    ```python
    code_scanner = CodeScanner()

    adafruit_account = {"username":"fuisl",
                        "key":"..."}
    code_scanner.set_ada_info(adafruit_account)
    ```

3. Connect to a camera with the `connect()` method:

    ```python
    code_scanner.connect()
    ```

4. Run the `scan()` method:

    ```python
    code_scanner.scan()
    ```

> *For now, threading is not yet implemented. Therefore, the `scan()` method can only be run one at a time, that means you can only scan either face or code at a time.*

### AdafruitIO Dashboard

- The AdafruitIO dashboard is hosted on `io.adafruit.com` by default. You can access the dashboard by entering the following URL in your browser:

    ```bash
    https://io.adafruit.com/fuisl/dashboards/checkin
    ```

### Reset Database

Reseting database is useful when you want to reset the checkin status of all tickets. This can be done by running the `reset_database.py` module. Beside reset database, you can create a new database. The configuration of the database is specified in `server.py`.

- reset_database.py is the main file for resetting the database. The module contains 2 functions:

  - `reset_is_bought()`: Reset is_bought status in ticket_data collection.
  - `reset_checked()`: Reset checkin status in ticket collection.

- To reset the database, import the module and run the functions:

    ```python
    from reset_database import reset_user, reset_ticket

    reset_is_bought()
    reset_checked()
    ```

## Demo

The system follow 3 main Phases:

1. Initialize Codes and Rendering
2. Get User Information/Ticket Information
3. Check-in

Refers to `bin/demo.ipynb` for full demonstration of the system devide into 3 steps.

## Troubleshooting

If you encounter any problems, please refer to the [Common Errors](https://github.com/fuisl/checkin/wiki/Common-Errors) section on the wiki page before submitting a GitHub issue.

## Acknowledgement