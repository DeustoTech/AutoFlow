
# Auto-Flow

![Status](https://img.shields.io/badge/Version-Experimental-brightgreen.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Introduction
------------
This repository presents an RPi-based platform to collect voiding events automatically with a microphone and machine learning. We hope this platform contributes towards performing non-intrusive sound-based uroflowmetry from acoustic energy.


## Table Of Contents ##

0. [Folder Structure](##Folder%20Structure)
1. [Lists of validated embedded devices](#List%20of%20validated%20devices)
3. [Support](#support)
4. [Platform pictures](#pictures)

##  Folder Structure ## 
-------------
- `RPi`: firmware to run the embedded device (such as the RPi), developped in Python
    - `keras_model`: Transfer Learning model saved in keras format
    - `tflite_model`: Transfer Learning model transformed to TFlite version
    - `ml_models`: traditional machine learning models

- `Server`: Restful Web Service developed with Flask and MongoDB. 
- `Beacon`: Configuration file for the EMBC2022 beacon 


## List of validated devices ##
--------------
The platform has been validated for real-time implementation on the following embedded devices. However, it does no mean that it is only compatible with these devices.
- RPi Zero 2 W (this one was used for final deployment)
- RPi Zero 2
- RPi 4 (A,B)
- RPi 3 (A,B)

## Support ##
--------------
- Contact [Laura Arjona] @DeustoTech through email `laura.arjona` at deusto.es
- Developed with Laura Arjona and Sergio, Hernandez, from the University of Deusto, Bilbao, Spain. Girish Narayanswamy from the University of Washington, Seattle, USA
 
- Collaborator: Dr. Elba Canelon, Puerta del Mar University Hospital, Cadiz, Spain.

## Pictures ##
--------------
<img src="https://github.com/DeustoTech/AutoFlow/tree/main/images/picture_beacon.jpg" width=50% height=50%>
![UroSound GUI](images/web1.png?raw=true "Title")
![UroSound GUI](images/web2.png?raw=true "Title")
![UroSound GUI](images/web3.png?raw=true "Title")

