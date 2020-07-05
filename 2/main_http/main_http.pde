#include <WaspWIFI_PRO.h>
#include <WaspFrame.h>
#include <WaspSensorCities_PRO.h>

uint8_t socket = SOCKET0;

Gas gas_sensor(SOCKET_1);

bmeCitiesSensor bme(SOCKET_2);


char type[] = "http";
char host[] = "192.168.1.159";
char port[] = "80";
char url[]  = "libelium_2";

uint8_t error;
uint8_t status;
unsigned long previous;

float temperature;
float humidity;
float pressure;
float concentration;  // Stores the concentration level in ppm

char temperature_str[25];
char pressure_str[25];
char humidity_str[25];

char concentration_str[25];

char dataToSend[110];


void remove_spaces(char* s) {
  const char* d = s;
  do {
    while (*d == ' ') {
      ++d;
    }
  } while (*s++ = *d++);
}

void setup()
{
  error = WIFI_PRO.ON(socket);

  if (error == 0)
  {
    USB.println(F("1. WiFi switched ON"));
  }
  else
  {
    USB.println(F("1. WiFi did not initialize correctly"));
  }

  status =  WIFI_PRO.isConnected();

  // check if module is connected
  if (status == true)
  {
    USB.println(F("2. WiFi is connected OK"));

    // get IP address
    error = WIFI_PRO.getIP();

    if (error == 0)
    {
      USB.print(F("IP address: "));
      USB.println( WIFI_PRO._ip );
    }
    else
    {
      USB.println(F("getIP error"));
    }
  }
  else
  {
    USB.print(F("2. WiFi is connected ERROR"));
  }

  error = WIFI_PRO.setURL( type, host, port, url );

  // check response
  if (error == 0)
  {
    USB.println(F("2. setURL OK"));
  }
  else
  {
    USB.println(F("2. Error calling 'setURL' function"));
    WIFI_PRO.printErrorCode();
  }
}


void loop()
{
  gas_sensor.OFF();

  bme.ON();

  temperature = bme.getTemperature();
  humidity = bme.getHumidity();
  pressure = bme.getPressure();

  bme.OFF();

  gas_sensor.ON();

  USB.println(F("Enter deep sleep mode to wait for electrochemical heating time..."));
  PWR.deepSleep("00:00:01:00", RTC_OFFSET, RTC_ALM1_MODE1, ALL_ON);
  USB.ON();
  USB.println(F("wake up!!"));

  // Read the electrochemical sensor and compensate with the temperature internally
  concentration = gas_sensor.getConc(temperature);

  dtostrf(humidity, 10, 6, humidity_str);
  dtostrf(pressure, 10, 6, pressure_str);
  dtostrf(temperature, 10, 6, temperature_str);
  dtostrf(concentration, 10, 6, concentration_str);

  remove_spaces(humidity_str);
  remove_spaces(pressure_str);
  remove_spaces(temperature_str);
  remove_spaces(concentration_str);

  sprintf(dataToSend, "co=%s&tp=%s&pr=%s&hu=%s", concentration_str, temperature_str, pressure_str, humidity_str);

  USB.print(dataToSend);

  USB.println(F("\n***************************************"));
  USB.print(F("Gas concentration: "));
  USB.printFloat(concentration, 3);
  USB.println(F(" ppm"));


  USB.print(F("Temperature: "));
  USB.printFloat(temperature, 3);
  USB.println(F(" Celsius degrees"));
  USB.print(F("RH: "));
  USB.printFloat(humidity, 3);
  USB.println(F(" %"));
  USB.print(F("Pressure: "));
  USB.printFloat(pressure, 3);
  USB.println(F(" Pa"));
  USB.println(F("***************************************"));

 error = WIFI_PRO.post(dataToSend);

  if (error == 0)
  {
    USB.print(F("3.1. HTTP POST OK. "));
    USB.print(F("HTTP Time from OFF state (ms):"));
    USB.println(millis() - previous);

    USB.print(F("\nServer answer:"));
    USB.println(WIFI_PRO._buffer, WIFI_PRO._length);
  }
  else
  {
    USB.println(F("3.1. Error calling 'post' function"));
    WIFI_PRO.printErrorCode();
  }

}

