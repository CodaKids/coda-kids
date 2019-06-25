# Coda Kids IDE Client Configuration

## Overview

Although the Coda Kids framework can be used in any python enviornment, We'd decided to create an entire IDE workflow for users using scripts. A breakdown of the tools used, with version numbers at time of writing:

- Python 3.5 installed through Miniconda 4.2
- Pygame 1.8.2 installed through Python 3.5’s default installed package control manager (pip)
- Visual Studio Code 1.8.1
- Pyinstaller through pip
- Pylint through pip
- Python Extension 0.5.5 installed through Visual Studio Code

Simply follow the instructions below for your target platform.

## Installation

### Windows

#### Testing

- [x] Windows 7
- [ ] Windows 8
- [x] Windows 10

#### Instructions

1. Unzip the downloaded Windows installation folder.
2. Open the unzipped folder.
3. Begin the installation by clicking the setup.bat file in the folder. It will install several things:
    - First, it will install Miniconda. This will take a couple of minutes.
    - Second, it will install Pygame.
    - Third, it will install Visual Studio Code. Follow the prompts and accept all the defaults.
    - After the script runs, it will launch Visual Studio Code. 
4. Follow the "Visual Studio Code Download" Link and download VS for your operating system.
5. Install the downloaded VS code installer.
6. Search for, install, and finally enable the Python plugin for Visual Studio Code.
7. Install coda_kids module by command line "python coda_kids install" in framework directory. coda_kids is a partial wrapper package around pygame. 

### Linux

#### Testing

- [x] Linux Mint
- [ ] Ubuntu

#### Instructions

NOTE: These instructions were written while installing on Linux Mint. These are subject to change as we test on other distributions.

1. Unzip the downloaded install folder.
2. Open the unzipped folder.
3. Locate the setup.sh file and right-click it. In the sub-context menu, select "Open With". Then select the "Run in Terminal" option.
4. A terminal will pop up, asking you to input your password, and then it will install several things:
    - First it will install Miniconda. This will take a couple of minutes.
    - Second, it will install Pygame.
    - Third it will install Visual Studio Code. Follow the prompts and accept all the defaults.
    - After the script runs, it might launch Visual Studio Code.
5. Important: You will need to update and restart Visual Studio Code.
6. Open Visual Studio Code and navigate to the Extensions tab.
7. Search for, install, and finally enable the Python plugin for Visual Studio Code.

### Mac

#### Testing

- [x] Mac OS X 10.11 EL Capitan

#### Instructions

1. Unzip the downloaded Mac installation folder.
2. Open the unzipped folder.
3. Right-click the setup file
4. From the sub-context menu, select Open With… -> Terminal
5. Input your user password. After successfully doing so, the script will install several things:
    - First, it will install Miniconda. This will take a couple of minutes.
    - Second, it will install Pygame.
    - Third, it will move Visual Studio Code to your apps folder.
    - After the script runs, it might launch Visual Studio Code.
6. Once the script is finished, open the Launchpad, find Visual Studio Code, and run it.
7. Navigate to the Extensions tab in Visual Studio Code.
8. Search for, install, and finally enable the Python plugin for Visual Studio Code.