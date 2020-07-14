# Installation Manual 

### SETUP GUIDE FOR SERVER AND MOBILE APPLICATION 

Kindly follow the steps below carefully to set up the application. 

**FIRST INSTALL THE OPERATING SYSTEM (UBUNTU 16.04)**

The server will be set up on a Linux distribution called Ubuntu. In this guide, we will be installing Ubuntu 16.04. However, the same installation process applies to Ubuntu 18.04 and Ubuntu 20.04 and the server set up is the same on all three versions of the Ubuntu operating system.

**For a Windows machine: **

Watch [this](https://www.youtube.com/watch?v=u5QyjHIYwTQ) video to learn how to install Ubuntu LTS alongside Windows OS (This is called [dual booting](https://en.wikipedia.org/wiki/Multi-booting)). 

Also see [this](https://www.forbes.com/sites/jasonevangelho/2018/08/29/beginners-guide-how-to-install-ubuntu-linux/#447509bb951c) link to learn how to install Ubuntu LTS alongside Windows.

**Support links**

See [1](https://itsfoss.com/install-ubuntu-1404-dual-boot-mode-windows-8-81-uefi/) or [2](https://askubuntu.com/questions/1031993/how-to-install-ubuntu-18-04-alongside-windows-10) or [3](https://hackernoon.com/installing-ubuntu-18-04-along-with-windows-10-dual-boot-installation-for-deep-learning-f4cd91b58557). 

**INSTALLING REQUIRED PACKAGES**

Now that a Ubuntu Operating system is set up. We would proceed to install the required packages:

The server is based on these main components:



1. [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) web framework.
2. [Flask-Assistant](https://flask-assistant.readthedocs.io/en/latest/) framework
3. [Google Assistant Service](https://developers.google.com/assistant/sdk/guides/service/python)
4. [MySQL](https://en.wikipedia.org/wiki/MySQL) database for storing all data. 
5. [Ngrok](https://ngrok.com/) tunneling service
6. [Python ](https://en.wikipedia.org/wiki/Python_(programming_language))Programming language. 

Let’s begin the installation



1. Open a web browser, preferably Google Chrome, Go to the [actions console](https://console.actions.google.com/) and choose create new project

2. After naming the project and choosing ok, look at the bottom of the screen and choose _Are you looking for device registration? Click here._ 

3. Click register model, give it a name and make the device type, phone

4. Select any traits and download the client json file

5. Enable the [API](https://console.developers.google.com/apis/api/embeddedassistant.googleapis.com/overview). Make sure to select the right project in the console

6. Click Enable

7. Configure the [OAuth consent screen](https://console.developers.google.com/apis/credentials/consent)

8. Choose External and click create

9. Choose the right support email and click Save

10. Go to project settings and **copy the Project ID**

11. Go to [https://console.actions.google.com/](https://console.actions.google.com/) and choose the project

12. Choose Develop and Choose Device Registration on the left

13. Click on the table and **copy the model id**

14. To download the OAuth file, click those three vertical dots on the extreme right of the product entry in the device registration table and choose the Download OAuth 2.0 credentials

15. Create a [dialogflow agent](https://dialogflow.cloud.google.com/). Follow the pictures below.

16. Click Entities on the left menu of the page

17. Click Create Entity

18. Enter each sensor value as an entry value, for each entry value, enter the same name for both the reference value and the synonym. An example is below

19. Click save

20. Click Intents on the left menu

21. Click Create intent

22. Put a new entry into the Actions and Parameters table

23. Make sure the entity name is the same entity name created in step 28

24. Enter the Training Phrases. For each phrase, the system will auto detect the entity names and highlight them as yellow. An example is below

25. Under responses, enable _Set the intent as end of conversation _

26. Under Fulfillment, enable _Enable webhook call for this intent_ and click SAVE

27. Click Integrations from the left menu, Click Integration settings 

28. Click TEST in the menu that pops up and actions console would open in a new tab

29. Record the project_id like in step 10 above. 

30. Download the complete code

31. Open web browser, preferably Google Chrome

32. Go to [https://github.com/RISC-NYUAD/calm_computing](https://github.com/RISC-NYUAD/calm_computing)

33. Click the Code button and download the Download Zip button (see below)

34. Right click on the calm_computing-master.zip folder in the Downloads folder and click Extract here. This is the complete server package

35. Right click on the extracted folder and click open in terminal 

36. In the opened terminal, enter bash install
*   `bash install`

37. Enter the computer password and press the Enter key, the installation will begin successfully if the computer is connected to the internet.

38. Enter the WiFi name to be used for this system, it should be the same WiFi that the phone, watch, Google Home and Libelium sensor boards are connected to.

39. Select the IP address to be used for the server and Click OK.

40. Enter the DialogFlow Project ID (called Project ID in the actions console below), refer to step 29

41. Enter the Device ID (called Project ID in the Actions console below), refer to step 10

42. Enter the Model ID, refer to step 13

43. Enter the password as root. Any other password will lead the installation to fail.
*   `root`

44. After entering root as the password, press the Tab key on the keyboard and press enter to proceed to enter the password one more time.

45. When the menu below pops up, navigate to the json file you downloaded in step 14

46. When the Authorization Code Prompt (in the picture below) shows up in the terminal, press CTRL on the keyboard and left click with the mouse on the link

47. Sign into your google account and click Allow

48. Press the copy button (the two nearly superimposed) next to the code

49. Paste it into the terminal (right click in terminal window and select Paste) and press Enter

50. Copy the link below and use it for step 53.

51. Copy the link below and paste it into a browser window to go the homepage

52. Open a new tab in a browser, preferably Google Chrome

53. Sign up for an [Ngrok account](https://dashboard.ngrok.com/signup), follow only step 1 and 2 in this [link](https://dashboard.ngrok.com/get-started/setup) and [Download ngrok](https://ngrok.com/download)

54. Unzip the file

55. Open a new terminal in the location of the downloaded file (right click on an empty space of the file window containing the ngrok downloaded file and select Open in Terminal).

56. Type the command in step 2 of this [link](https://dashboard.ngrok.com/get-started/setup) (this is specific to your ngrok account so it will ask you to sign in if you are not already signed in)

57. Enter the link from step 50 and press Enter. In case one did not save the link in step 50, a template is shown below, replace **ip_address** with the IP address used for the system
*   <code>./ngrok http http://<strong>ip_address</strong>:80</code>

58. In the sensorReadings project in DialogFlow, Click Fulfilment on the left menu of the page
59. Copy the URL from the ngrok terminal, the https one. It should look like this _[https://someValue.ngrok.io](https://68b6d824a7db.ngrok.io)_

60. Paste the URL and into the URL* box of the Fulfillment page in the web browser and Click Save. Make sure it saves by refreshing the page to see if the URL is still in the box. If it isn’t, enter the URL and Click save again.

**WASPMOTE & PLUG & SENSE**



1. Set up [Waspmote](http://www.libelium.com/development/waspmote/documentation/waspmote-quick-start-guide/) ([http://www.libelium.com/development/waspmote/documentation/waspmote-quick-start-guide/](http://www.libelium.com/development/waspmote/documentation/waspmote-quick-start-guide/))

2.  Set up [Plug & Sense](http://www.libelium.com/development/plug-sense/documentation/waspmote-plug-sense-technical-guide/) ([http://www.libelium.com/development/plug-sense/documentation/waspmote-plug-sense-technical-guide/](http://www.libelium.com/development/plug-sense/documentation/waspmote-plug-sense-technical-guide/))

3. Connect the sensors carefully by following the documentation of Waspmote and Plug & Sense above respectively.

1. Sensors on Plug & Sense ([http://www.libelium.com/downloads/documentation/waspmote_plug_and_sense_sensors_guide.pdf](http://www.libelium.com/downloads/documentation/waspmote_plug_and_sense_sensors_guide.pdf))
        1. Temperature
        2. Humidity
        3. Pressure

    1. Sensors on Waspmote 
        1. Carbon monoxide 
        2. Temperature
        3. Pressure
        4. Humidity



4. Install [Waspmote Pro IDE](http://www.libelium.com/development/plug-sense/sdk_applications/) (http://www.libelium.com/development/plug-sense/sdk_applications/) ( for Windows / Linux /Mac. Follow this [guide](http://www.libelium.com/development/waspmote/documentation/ide-user-guide/)** **(http://www.libelium.com/development/waspmote/documentation/ide-user-guide/)
1. For Plug & Sense:
    1. Plug the sensor board into the USB port
    2. Open the program [WIFI_PRO_01_configure_essid.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/1/WIFI_PRO_01_configure_essid/WIFI_PRO_01_configure_essid.pde) in the folder calm_computing-master/1/WIFI_PRO_01_configure_essid with Waspmote and Upload the code to the board (upload button at top left circled in the picture below). Wait for 3 minutes

    3. Open the program [WIFI_PRO_02_join.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/1/WIFI_PRO_02_join/WIFI_PRO_02_join.pde) in the folder calm_computing-master/1/WIFI_PRO_02_join with Waspmote and Upload the code to the board (upload button at top left circled in the picture below). Wait for three minutes

    4. Open the program [main_http.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/1/main_http/main_http.pde) in the folder calm_computing-master/1/main_http with Waspmote and Upload the code to the board (upload button at top left circled in the picture below). Wait for three minutes

2. For the Waspmote:
    5. Plug the sensor board into the USB port
    6. Open the program [WIFI_PRO_01_configure_essid.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/2/WIFI_PRO_01_configure_essid/WIFI_PRO_01_configure_essid.pde) in the folder calm_computing-master/2/WIFI_PRO_01_configure_essid with Waspmote and Upload the code to the board (upload button at top left circled in the picture below). Wait for three minutes

    7. Open the program [WIFI_PRO_02_join.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/2/WIFI_PRO_02_join/WIFI_PRO_02_join.pde) in the folder calm_computing-master/2/WIFI_PRO_02_join with Waspmote and Upload the code to the board (upload button at top left circled in the picture below). Wait for three minutes

    8. Open the program [main_http.pde](https://github.com/RISC-NYUAD/calm_computing/blob/master/2/main_http/main_http.pde) in the folder calm_computing-master/2/main_http with Waspmote and Upload the code to the board (upload button at top left circled in the picture below). Wait for three minutes

**Serial port issues**



*   In case one runs into issues with serial port errors, make sure you have selected the correct serial port

*   After trying the step above, if one still has issues, try this command and replace the last character X with the number after /dev/ttyUSBX in their waspmote as shown above.

**SETTING UP AND OPERATING THE MOBILE APPLICATION**



*   Install the mobile application with the APK file (app-release.apk) in [this](https://github.com/RISC-NYUAD/spaigh/blob/master/app/release/app-release.apk) github repository. Download the file as shown below, and then install it after downloading.

*   Make sure that the smartphone and the server are connected to the same network. 

*   On opening the application, after installation, type <code>[http://server_ip_address/phone_1](http://server_ip_address/phone_1)</code>  inside the text box hinting server address. Note that one has to replace <strong><code>server_ip_address</code></strong> in the URL above with the IP address that we found in the last step of setting up the server. 

*   Now click on the <strong>Start Service </strong>button to start the application and watch out for the toasts that pop up. 

*   One will be prompted to grant some permissions to the application. Click accept. The application will not run properly without these permissions being granted. 

*   After granting the permissions, the application should say <strong>service is running</strong> at the top of the and a <strong>foreground notification</strong> should show up at the top of the screen. 

*   The application is now fully set and one can head over to the browser and type URL <code>[http://server_ip_address/phone_1](http://server_ip_address/phone_1)</code> to check the current state of the phone at any period. Replace server_ip_address with the IP address used for the server in the prior steps.

*   Also, the application User Interface allows one to see the state of the device in real-time.

*   Note that one can close the application and the application will run as a notification in the foreground.

*   To stop the application, open the application, and click <strong>stop service.</strong>

<strong>SETTING UP AND OPERATING THE SMARTWATCH APPLICATION</strong>



*   Install the watch app using the TPK file in [this](https://google.com) folder.

*   Launch the application after installation and one will be required to grant the application permissions to access the device’s sensors (Heart rate sensor in our case). Click the “check mark” sign to grant permission. Note that the app will not work without the permission being granted. 

*   Enter the IP address of the server into the text box that hints “Enter IP address here.”

*   Click the **Connect** button.

*   Then enter the time interval in which you would like to measure and report the heart rate reading (in seconds). Default value is 30 seconds. 

*   Click the **Connect** button. 

*   The application will run if the watch has an active internet connection (Wi-Fi, ethernet, or mobile(LTE)) and the server is running.

*   If one gets an error message that says “**Cannot Connect**”, then that indicates that there is a problem with the server or the watch’s internet connection.

*   One might also get an error message that reads “**No Internet Connection**” which basically indicates that one does not have an active internet connection.

*   One might also want to ensure that they entered in the correct IP address in the address box if one gets a “**Cannot Connect**” error message.

*   If on the other hand, one has an active internet connection, one entered the correct IP address for the server and the server is up and running, then one would be taken to the next screen.

*   Click on the **Start** button to start recording the heart rate data and having it automatically sent to the server.

*   On clicking the Start button, the application would print a toast message: **Heart Rate Monitoring Started**. If one gets an error message, follow the instructions given by the error message.

*   One can leave the app and the app will keep running in the background.

*   One can also always go back to the app and click the **Stop** button to stop the app from recording heart rate data.

*   On stopping the app, the application would print a toast message: **Heart Rate Monitoring Stopped. **

### UNDERSTANDING THE PHONE’S DATA 



**ALLOWED DEVICE MOTION STATES** 

*   **DEVICE IDLE:** This indicates that the phone is not moving.

*   **DEVICE MOVING:** This indicates that the phone is moving. 

**ALLOWED CALL STATES**

*   **CALL-IDLE:** This indicates that the user is not having a call and the phone is not ringing. 

*   **CALL-ACTIVE:**This indicates that the user has accepted an incoming call. 

*   **RINGING:** This indicates that the user has an incoming call that has not been picked up yet.

*   **OUTGOING CALL:** This indicates that the user is making an outgoing call. 
