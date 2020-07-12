# Calm_Computing  


## SETUP GUIDE FOR SERVER AND MOBILE APPLICATION 

Kindly follow the steps below carefully to set up your application. 

**WASPMOTE & PLUG & SENSE**



1. Install [Waspmote Pro IDE](http://www.libelium.com/development/plug-sense/sdk_applications/) for Windows / Linux /Mac. Follow this [guide](http://www.libelium.com/development/waspmote/documentation/ide-user-guide/)
2. For ease, you should use a seperate computer for each sensor board, Waspmote and Plug & Sense
3. Open [app.py](https://github.com/RISC-NYUAD/calm_computing/blob/master/calm_com/app.py), change the IP address in line 799 to the correct IP address. Find the IP address of the Linux server by checking this [link](https://tecadmin.net/check-ip-address-ubuntu-18-04-desktop/)
4. For Waspmote connected to computer 1:
    1. Open the program [WIFI_PRO_01_configure_essid.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/1/WIFI_PRO_01_configure_essid/WIFI_PRO_01_configure_essid.pde), change the variable ESSID and the PASS in line 11 to the Wifi Name and Password of the router. Upload the code to the board
    2. Open the program [WIFI_PRO_02_join.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/1/WIFI_PRO_02_join/WIFI_PRO_02_join.pde), change the IP address in line 65 to the IP address found in step 3. Upload the code to the board
    3. Open the program [main_http.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/1/main_http/main_http.pde), change the IP address in line 8 to the IP address found in step 3 above. Upload the code to the board
5. For the Plug & Sense connected to computer 2:
    1. Open the program [WIFI_PRO_01_configure_essid.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/2/WIFI_PRO_01_configure_essid/WIFI_PRO_01_configure_essid.pde), change the variable ESSID and the PASS in line 11 to the Wifi Name and Password of the router. Upload the code to the board
    2. Open the program [WIFI_PRO_02_join.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/2/WIFI_PRO_02_join/WIFI_PRO_02_join.pde), change the IP address in line 65 to the IP address found in step 3. Upload the code to the board
    3. Open the program [main_http.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/2/main_http/main_http.pde), change the IP address in line 13 to the IP address found in step 3 above. Upload the code to the board

     


**SETTING UP THE SERVER**

This application utilizes client-server architecture. What that simply means is that the application requires a client (the mobile application or the sensors' firmware) and a [server](https://en.wikipedia.org/wiki/Server_(computing)) in order to work correctly. Therefore it is required that we set up the server properly in order to be able to receive and visualize data from our mobile application and the libelium sensors. If this is your first time setting up a server, you are in good hands, this guide will walk you through the process.

**FIRST INSTALL THE OPERATING SYSTEM (UBUNTU 16.04)**

The server will be set up on a Linux distribution called Ubuntu. In this guide, we will be installing Ubuntu 16.04. However, the same installation process applies to Ubuntu 18.04 and Ubuntu 20.04 and the server set up is the same on all three versions of the Ubuntu operating system.

If you already have a Ubuntu operating system running then you should skip this step. If you do not, then follow the guides below to install Ubuntu 16.04 LTS on your machine:

**For a Windows machine: **

Watch [this](https://www.youtube.com/watch?v=u5QyjHIYwTQ) video to learn how to install Ubuntu 18.04 LTS alongside your Windows OS (This is called [dual booting](https://en.wikipedia.org/wiki/Multi-booting)). 

Also see [this](https://www.forbes.com/sites/jasonevangelho/2018/08/29/beginners-guide-how-to-install-ubuntu-linux/#447509bb951c) link to learn how to install Ubuntu 16.04 LTS alongside Windows.

**Support links**

See [1](https://itsfoss.com/install-ubuntu-1404-dual-boot-mode-windows-8-81-uefi/) or [2](https://askubuntu.com/questions/1031993/how-to-install-ubuntu-18-04-alongside-windows-10) or [3](https://hackernoon.com/installing-ubuntu-18-04-along-with-windows-10-dual-boot-installation-for-deep-learning-f4cd91b58557). 

**INSTALLING REQUIRED PACKAGES**

Now that you have a Ubuntu Operating system set up. Congratulations! We would proceed to install the required packages for our server to run properly:

The server is based on these main components:



1. [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) web framework.
2. [Flask-Assistant](https://flask-assistant.readthedocs.io/en/latest/) framework
3. [Google Assistant Service](https://developers.google.com/assistant/sdk/guides/service/python)
4. [MySQL](https://en.wikipedia.org/wiki/MySQL) database for storing all data. 
5. [Ngrok](https://ngrok.com/) tunneling service
6. [Python ](https://en.wikipedia.org/wiki/Python_(programming_language))Programming language. 

Let’s begin the installation



1. Go to the [actions console](https://console.actions.google.com/) and choose create new project

2. After naming the project and choosing ok, look at the bottom of the screen and choose _Are you looking for device registration? Click here._ 

This is the link in case it disappears in the future. (https://console.actions.google.com/project/**device_id**/deviceregistration/). Replace **device_id** in the URL with your device’s id. Find the device id by checking step **10**



3. Click register model, give it a name and make the device type, phone
4. Select any traits you like and download the client json file
5. Enable the [API](https://console.developers.google.com/apis/api/embeddedassistant.googleapis.com/overview). Make sure you have selected the right project in the console
6. Click Enable
7. Configure the [OAuth consent screen](https://console.developers.google.com/apis/credentials/consent)
8. Choose External and click create
9. Choose the right support email and click Save
10. Go to project settings and **copy the Project ID**
11. Go to [https://console.actions.google.com/](https://console.actions.google.com/) and choose the project
12. Choose Develop and Choose Device Registration on the left
13. Click on the table and **copy the model id**
14. To download the OAuth file, click those three vertical dots on the extreme right of the product entry in the device registration table and choose the Download OAuth 2.0 credentials
15. Open a terminal and enter the following commands, one after the other
*   `sudo apt update && sudo apt upgrade`
*   `ifconfig`
*   `update-alternatives --remove python /usr/bin/python2`
*   `sudo update-alternatives --remove python /usr/bin/python2`
*   `update-alternatives --install /usr/bin/python python /usr/bin/python3 10`
*   `sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10`
16. Check python version, make sure it is python 3.4 or above by typing


```
python --version

```



17. Let’s continue, in the terminal window, enter the following commands, one after the other
*   `sudo apt-get update`
*   `sudo apt-get install python3-dev python3-venv`
*   `python3 -m venv env`
*   `env/bin/python -m pip install --upgrade pip setuptools wheel`
*   `source env/bin/activate`
*   `sudo apt-get install portaudio19-dev libffi-dev libssl-dev`
*   `python -m pip install --upgrade google-assistant-sdk[samples]`
*   `python -m pip install --upgrade google-auth-oauthlib[tool]`
18. Enter the command below
*   <code>google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save --headless --client-secrets <strong>paths_to_json_file</strong></code>
19. Replace <strong>paths_to_json_file</strong> with path to downloaded OAtuh file: most probably something that looks like this ~/Downloads/<em>something</em>.json
20. Click the link that appears in the terminal and when the browser opens, choose allow, copy the code that appears and paste it back into the terminal and press Enter on your keyboard
*   <code>sudo apt install authbind</code>
*   <code>sudo touch /etc/authbind/byport/80</code>
*   <code>sudo chmod 777 /etc/authbind/byport/80</code>
*   <code>source /home/nuc/env/bin/activate</code>
*   <code>pip install flask-assistant</code>
21. I will share the google cloud project with you from [princesannor@gmail.com](mailto:princesannor@gmail.com) so no need to create a new one but if you want to build it from scratch, see below. The project id of this shared project will be <em>sensorreadings-qccmpb</em>
    1. Create a [conversational project](https://www.youtube.com/watch?v=HipsHUsSvjQ), call it sensorReadings if you like, in [actions console](https://console.actions.google.com/). Record the project_id like in step 10 above.
    2. Link the project with [DialogFlow](https://www.youtube.com/watch?v=z5f52sMgJLQ)
    3. In Dialog flow, click Entities on the left menu of the page
    4. Click Create Entity
    5. Enter each sensor value as an entry value, for each entry value, enter the same name for both the reference value and the synonym 
    6. Click save
    7. Click Intents
    8. Click Create intent
    9. Put a new entry into the Actions and Parameters table
    10. Make sure the entity name is the same entity name you created in step 28
    11. Enter the Training Phrases. For each phrase, the system will auto detect the entity names and highlight them as yellow
    12. Under responses, enable <em>Set the intent as end of conversation </em>
    13. Under Fulfillment, enable <em>Enable webhook call for this intent</em>
22. Open a new tab in your browser
23. Sign up for an [Ngrok account](https://dashboard.ngrok.com/signup), follow step 1 and 2 in this [link](https://dashboard.ngrok.com/get-started/setup) and [Download ngrok](https://ngrok.com/download)
24. Open a new terminal and enter the command below, replace <strong>ip_address </strong>with your ip_address. Look at this [link](https://tecadmin.net/check-ip-address-ubuntu-18-04-desktop/) to find your <strong>ip_address</strong>
*   <code>./ngrok http http://<strong>ip_address</strong>:80</code>
25. In the sensorReadings project in DialogFlow, Click Fulfilment on the left menu of the page
26. Copy the URL from the ngrok terminal, the https one. Looks like something like this <em>[https://68b6d824a7db.ngrok.io](https://68b6d824a7db.ngrok.io)</em>
27. Paste the URL and into the URL* box of the Fulfillment page in the web browser and Click Save. Make sure it saves by refreshing the page to see if the URL is still in the box. If it isn’t, enter the URL and Click save again.
28. Open the file textinput.py, go to line 98
    14. Change the value of the device_model_id variable to the device_model_id you saved in step 13
    15. Change the value of the device_id variable to the project_id you saved in step 10
    16. Save both files
29. Install the MySQL database. Follow only <strong>step 1</strong> and <strong>step 2 </strong>of [this](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) guide to install the MySQL database. Make sure to remember the [root user](https://en.wikipedia.org/wiki/Superuser) password that you set when installing the MySQL database. 


### SETTING UP THE DATABASE

Type in the following into a command line (press ctrl+alt+t to open a command line):

	 `mysql -u root -p`

Enter the root password, that you set when installing the MySQL database, when prompted and press enter. 

Now let’s create a database where we will store all the tables required for our incoming data. Type/copy and run the below command in the MySQL terminal which opened after entering your password above (make sure to also type/copy the semicolon)

	 `CREATE DATABASE calm_computing;`

Now we move on to creating the appropriate tables and setting up the required columns in those tables. Run the following in the MySQL terminal:

*  <code><strong> USE calm_computing; </strong></code> 


```
     CREATE TABLE calm_computing.mlibelium_1(id int AUTO_INCREMENT, date varchar(30), time varchar(30), temperature varchar(30), pressure varchar(30), humidity varchar(30), lux varchar(30), lumen varchar(30), primary key(id));

     CREATE TABLE calm_computing.mlibelium_2(id int AUTO_INCREMENT, date varchar(30), time varchar(30), CO varchar(30), temperature varchar(30), pressure varchar(30), humidity varchar(30), primary key(id));

     CREATE TABLE calm_computing.mwatch_1(id int AUTO_INCREMENT, date varchar(30), time varchar(30), heart_rate varchar(30), primary key(id));

     CREATE TABLE calm_computing.mphone_1(id int AUTO_INCREMENT, date varchar(30), time varchar(30), device_state varchar(30), call_state varchar(30), primary key(id));
```


And we are done with the database! Type `exit `to quit the MySQL terminal. 

### INSTALLING CONNECTING LIBRARIES AND DEPENDENCIES

In the terminal, type:


```
 source my_env/bin/activate.
```


The above command takes you into the virtual environment you created earlier. Note that<code> <strong>my_env</strong></code> is the name you set up [here](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart#step-6-%E2%80%94-create-a-virtual-environment). If you encounter any errors running this command, type in the full path to the virtual environment. 

Now in the virtual environment run each of  the commands sequentially:


```
     pip3 install wheel
     sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
     sudo apt-get install libmysqlclient-dev
     pip3 install flask-mysqldb

     pip install pyyaml

     pip3 install mysql-connector-python-rf
     sudo apt-get install python-mysqldb
     wget http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.1.6.tar.gz
     tar -xf mysql-connector-python-2.1.6.tar.gz
     cd mysql-connector-python-2.1.6/
     sudo python3 setup.py install

     pip3 install pygal 
```


	

Okay, now we are finally done with the server-side, technically. 

### SETTING UP AND OPERATING THE MOBILE APPLICATION



*   Install the mobile application with the APK file in [this](https://drive.google.com/drive/folders/1SKiIlpzRpZ03IdIGXjyv3uTgY7qAw4oO?usp=sharing) shared google drive folder. 

*   Make sure that your smartphone and the server are connected to the same network. 

*   On opening the application, after installation, type <code>[http://server_ip_address/phone_1](http://server_ip_address/phone_1)</code>  inside the text box hinting server address. Note that you have to replace <strong><code>server_ip_address</code></strong> in the URL above with the IP address that we found in the last step of setting up the server. 

*   Now click on the <strong>START SERVICE </strong>button to start the application and watch out for the toasts that pop up. 

*   You will be prompted to grant some permissions to the application. Click accept. The application will not run properly without these permissions being granted. 

*   After granting the permissions, your application should say <strong>service is running</strong> at the top of the and a <strong>foreground notification</strong> should show up at the top of your screen. 

*   Your application is now fully set and you can head over to your browser and type URL <code>[http://server_ip_address/phone_1](http://server_ip_address/phone_1)</code> to check the current state of your phone at any period. 

*   Also, the application User Interface allows you to see the state of the device in real-time.

*   Note that you can close the application and the application will run as a notification in the foreground.

*   To stop the application, open the application, and click <strong>STOP SERVICE.</strong> 

<strong>ACCESSING THE LIBELIUM SENSORS’ DATA</strong>



*   Enter the below URL into a web browser to access realtime data for the libelium sensors and the smartphone:

*   	<code>[http://server_ip_address/home](http://server_ip_address/home)</code> 


    Note that you have to replace <strong><code>server_ip_address</code></strong> in the URL above with the IP address that we found in the last step of setting up the server.


### SETTING UP AND OPERATING THE SMARTWATCH APPLICATION


* Install the watch app using the TPK file in [this](https://google.com) folder.

* Launch the application after installation and you will be required to grant the application permissions to access your device’s sensors (Heart rate sensor in our case). Click the “check mark” sign to grant permission. Note that the app will not work without the permission being granted. 

* Enter the IP address of the server into the text box that hints “Enter IP address here.”

* Click the <strong>Connect</strong> button.

* The application will run if your watch has an active internet connection (Wi-Fi, ethernet, or mobile(LTE)) and the server is running.

* If you get an error message that says <strong> Cannot Connect</strong>, then that indicates that there is a problem with the server or the watch’s internet connection.

* You might also get an error message that reads <strong>No Internet Connection</strong> which basically indicates that you do not have an active internet connection.

* You might also want to ensure that you entered in the correct IP address in the address box if you get a <strong> Cannot Connect</strong> error message.

* If on the other hand, you have an active internet connection, you entered the correct IP address for the server and the server is up and running, then you would be taken to the next screen.

* Click on the <strong> Start</strong> button to start recording your heart rate data and having it automatically sent to the server.

* On clicking the <strong>Start</strong> button, the application would print a toast message: <strong>Heart Rate Monitoring Started</strong>. If you get an error message, follow the instructions given by the error message.

* You can leave the app and the app will keep running in the background.

* You can also always go to the app and click the <strong>Stop</strong> button to stop the app from recording heart rate data.

* On stopping the app, the application would print a toast message:  <strong>Heart Rate Monitoring Stopped</strong>. 


### UNDERSTANDING THE PHONE’S DATA



*   **ALLOWED DEVICE MOTION STATES**

        **DEVICE IDLE:** This indicates that the phone is not moving.


        **DEVICE MOVING:** This indicates that the phone is moving. 

*   **ALLOWED CALL STATES** 

        **CALL-IDLE:** This indicates that the user is not having a call and the phone is not ringing. 


        **CALL-ACTIVE:** This indicates that the user has accepted an incoming call. 


        **RINGING:** This indicates that the user has an incoming call that has not been picked up yet.


        **OUTGOING CALL:** This indicates that the user is making an outgoing call.

