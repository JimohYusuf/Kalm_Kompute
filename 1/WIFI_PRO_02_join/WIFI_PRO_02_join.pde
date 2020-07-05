#include <WaspWIFI_PRO.h>


// choose socket (SELECT USER'S SOCKET)
///////////////////////////////////////
uint8_t socket = SOCKET0;
///////////////////////////////////////


uint8_t error;
uint8_t status;
unsigned long previous;



void setup() 
{
  USB.ON();
  USB.println(F("Start program"));  
  USB.println(F("***************************************"));  
  USB.println(F("Once the module is set with one or more"));
  USB.println(F("AP settings, it attempts to join the AP"));
  USB.println(F("automatically once it is powered on"));    
  USB.println(F("Refer to example 'WIFI_PRO_01' to configure"));  
  USB.println(F("the WiFi module with proper settings"));
  USB.println(F("***************************************"));

  //////////////////////////////////////////////////
  // 1. Switch ON
  //////////////////////////////////////////////////  
  error = WIFI_PRO.ON(socket);

  if (error == 0)
  {    
    USB.println(F("1. WiFi switched ON"));
  }
  else
  {
    USB.println(F("1. WiFi did not initialize correctly"));
  }  

  // get current time
  previous = millis();  
}



void loop()
{

  //////////////////////////////////////////////////
  // 2. Join AP
  //////////////////////////////////////////////////  

  // check connectivity
  status =  WIFI_PRO.isConnected();

  // Check if module is connected
  if (status == true)
  { 
    USB.print(F("2. WiFi is connected OK."));
    USB.print(F(" Time(ms):"));    
    USB.println(millis()-previous);

    error = WIFI_PRO.ping("192.168.1.159");

    if (error == 0)
    {				
      USB.print(F("3. PING OK. Round Trip Time(ms)="));
      USB.println( WIFI_PRO._rtt, DEC );
    }
    else
    {
      USB.println(F("3. Error calling 'ping' function")); 
    }
  }
  else
  {
    USB.print(F("2. WiFi is connected ERROR.")); 
    USB.print(F(" Time(ms):"));    
    USB.println(millis()-previous);  
  }

  delay(10000);
}
