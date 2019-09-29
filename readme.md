
**Requirements**

1. OS Ubuntu 18.04.2 LTS


    1.1 Check version ` lsb_release -a`, result:
       
        No LSB modules are available.
        Distributor ID: Ubuntu
        Description:    Ubuntu 18.04.2 LTS
        Release:        18.04
        Codename:       bionic

2. Install Alsa Library:

    Alsa Library is the binding factor between pyaudio and portaudio.

    `sudo apt-get install libasound-dev`

3. Install PortAudio Library:

    3.1 `cd dependencies`
    
    3.2 `tar xvfz pa_stable_v190600_20161030.tgz`
    
    3.3 `./configure`
    
    3.4 `make`
    
    3.5 `sudo make install`
    
    3.6 `sudo ldconfig`

4 Python 3.6.8 in build in OS:

   4.1 Check version `python --version`, result:
    
        Python 3.6.8

   4.2 Install pip:
   
   `sudo apt install -y python3-pip`
        
   4.3 Install dependencies:
   
   `sudo apt install build-essential libssl-dev libffi-dev python3-dev`
        
   4.4 Install virtual environment:
   
   `sudo pip3 install virualenv virtualenvwrapper`
        
   4.5 Setting up virtual environment
   
   4.5.1 Setting up terminal interface, add in the EOF of ~/.bachrc next lines:
            
            export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
            export WORKON_HOME=$HOME/.virtualenvs
            export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
            source /usr/local/bin/virtualenvwrapper.sh
        
   4.5.2 Reopen terminal and run next command:
        
   `mkvirtualenv signalp`

   4.6 Install all project dependencies:
   
   `pip install requirements.txt`
   
        