### WASPMOTE & PLUG & SENSE



1. Turn on the Waspmote switch and the Plug & Sense switch

**STARTING THE SERVER**



1. Open a new terminal, cd to the location to the ngrok binary, and enter the command below, replace **ip_address **with the ip_address used for the setup.
*   <code>./ngrok http http://<strong>ip_address</strong>:80</code>

2. Open a new tab in your browser

3. In the sensorReadings project in DialogFlow, Click Fulfilment on the left menu of the page

4. Copy the URL from the ngrok terminal, the https one. Looks like something like this _[https://68b6d824a7db.ngrok.io](https://68b6d824a7db.ngrok.io)_

5. Paste the URL and into the URL* box of the Fulfillment page in the web browser and Click Save. Make sure it saves by refreshing the page to see if the URL is still in the box. If it isn’t, enter the URL and Click save again.

6. Open another terminal and enter the command below
*   `bash runserver`

7. Open a web browser and enter the address **ip_address/home**:80, replace **ip_address** with the server’s IP address.

8. The first button lets you set the actions that should happen when a specific sensor value is surpassed. Hit submit when done.

9. The rest of the buttons give you plots and tables of the various sensors and of the phone. See pictures below.

10. You can also download the data as csv files using the last two buttons

**DIRECTLY ACCESS AND MODIFY THE DATABASE**



1. Open another terminal and enter the command below to access the database. You don’t need to do this to start the program, but in case you need to query or modify the database in the future
*   `mysql -u root -p`

2. Enter the password (default is root)

3. Select the database
*   `Use calm_computing`

4. Query table one (mlibelium_1)
*   `select * from mlibelium_1;`

5. Query table one (mlibelium_2)
*   `select * from mlibelium_2;`

6. To safely exit the database system and return to the command line, type 
*   `exit`

**MOBILE APPLICATION OPERATION**



1. Launch the application by clicking its launcher icon from your application list. The start screen will come up. 

2. Enter the server address

3. Press the “START SERVICE” button. You’ll be prompted to grant the application Phone permissions.

4. After granting permissions, the service will start by showing you the connection state and displaying a toast message “service started”. You’ll also see the foreground notification icon at the top of your screen. 

5. To stop the service, click on the “STOP SERVICE” button. You’ll then see the initial startup screen again.


**WATCH APPLICATION OPERATION**



*   Launch the application after installation and you will be required to grant the application permissions to access your device’s sensors (Heart rate sensor in our case). Click the “check mark” sign to grant permission. Note that the app will not work without the permission being granted. 

*   After granting permissions, you will be directed to the welcome and connect screen. 

*   Enter the IP address of the server into the text box that hints “enter ip address here.”

*   Click the **Connect** button.

*   Then enter the time interval in which you would like to measure and report the heart rate reading (in seconds). Default value is 30 seconds. 

*   Click the **Connect** button. 

*   The application will run if your watch has an active internet connection (Wi-Fi, ethernet, or mobile(LTE)) and the server is running.

*   If you get an error message that says “**Cannot Connect**”, then that indicates that there is a problem with the server or the watch’s internet connection.

*   You might also get an error message that reads “**No Internet Connection**” which basically indicates that you do not have an active internet connection.

*   You might also want to ensure that you entered in the correct IP address in the address box if you get a “**Cannot Connect**” error message.

*   If on the other hand, you have an active internet connection, you entered the correct IP address for the server and the server is up and running, then you would be taken to the next screen.

*   Click on the **Start** button to start recording your heart rate data and having it automatically sent to the server.

*   On clicking the Start button, the application would print a toast message: **Heart Rate Monitoring Started**. If you get an error message, follow the instructions given by the error message.

*   After the toast message, the app will then show the Heart Rate value in beats per minute (bpm) on the screen.

*   You can leave the app and the app will keep running in the background.

*   You can also always go back to the app and click the **Stop** button to stop the app from recording heart rate data.
* On stopping the app, the application would print a toast message: **Heart Rate Monitoring Stopped.** 

**SYSTEM USE CASE**


* Here, we are going to present a use case scenario for the system which we have built so far. Everything we are going to present here can be found in [this](https://drive.google.com/file/d/1S-f0tatsOfERA_kvf6cCITm2riajSulr/view?usp=sharing) video.


**ENVIRONMENTAL SENSORS (CASE 1)**


* Though everyone might have unique preferences for what they refer to as being “calm”, we still generally share some of those preferences. We are going to try to simulate some possible use scenarios for the system defined above to demonstrate just how we might be able to achieve a calm environment using the system which we have described in the previous sections.


* The libelium sensors have temperature, humidity, luminosity, illuminance, CO level and pressure sensors. Let’s say we define calm to be:


*   Temperature less than 25 degrees celsius and greater than 17 degrees celsius

*   Humidity less that 60% and greater than 15% 

*   Pressure as 100,000 ∓ 2000 Pa

*   CO level less than 0.3 ppm

*   Illuminance less than 1000 lux

*   Luminosity less than 1000 lumens

	To implement this, you simply go to the system’s web page:


    http://**server_ip_address**/home


    Then click on the “Set Extreme Values and Configure Actions Button”


    You will be presented with a page that allows you to set the extreme values for each sensor and here is the interesting part, you will also be able to select an action that you would like to happen when an extreme condition is met. 


    Click submit and that is all. Whenever an extreme value is met, the action you selected is carried out. You can always go back to the extreme value page and change your settings. 


    **SMARTPHONE APPLICATION (CASE 2)**


    Now let’s say you would like your house an automated “calm” environment, and part of what you define as calm is your TV or speaker’s audio being reduced whenever you are making a call. Well all you have to do is configure that action in the configuration page. 


    VALUE: Phone ringing


    ACTION: Reduce smart speaker volume to 5% or turn off TV


    And that is all you have to do. Now whenever your phone is ringing, you the system checks whether your smart speaker is ON and if its volume is greater than 5%. If this is the case, it reduces the volume to 5%. 


    See demo video [here](https://drive.google.com/file/d/1S-f0tatsOfERA_kvf6cCITm2riajSulr/view?usp=sharing). Demo video only covers case 1 but can also be applied to case 2. 