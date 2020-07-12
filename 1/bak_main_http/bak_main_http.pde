#include <WaspWIFI_PRO.h>
#include <WaspFrame.h>
#include <WaspSensorAmbient.h>

uint8_t socket = SOCKET0;

char type[] = "http";
char host[] = "replace_the_ip_address";
char port[] = "80";
char url[]  = "libelium_1";

uint8_t error;
uint8_t status;
unsigned long previous;

float temperature;
float humidity;
float pressure;

float analogLDRvoltage;

uint32_t digitalLuxes;

char temperature_str[25];
char pressure_str[25];
char humidity_str[25];

char analogLDRvoltage_str[25];

char digitalLuxes_str[25];

char dataToSend[135];

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
  USB.ON();
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

  temperature = SensorAmbient.getTemperatureBME();
  humidity = SensorAmbient.getHumidityBME();
  pressure = SensorAmbient.getPressureBME();

  analogLDRvoltage = SensorAmbient.getLuminosity();

  digitalLuxes = SensorAmbient.getLuxes(INDOOR);

  dtostrf(humidity, 14, 6, humidity_str);
  dtostrf(pressure, 14, 6, pressure_str);
  dtostrf(temperature, 14, 6, temperature_str);
  dtostrf(analogLDRvoltage, 14, 6, analogLDRvoltage_str);
  dtostrf(float(digitalLuxes), 14, 6, digitalLuxes_str);

  remove_spaces(humidity_str);
  remove_spaces(pressure_str);
  remove_spaces(temperature_str);
  remove_spaces(analogLDRvoltage_str);
  remove_spaces(digitalLuxes_str);

  sprintf(dataToSend, "tp=%s&pr=%s&hu=%s&lx=%s&lm=%s", temperature_str, pressure_str, humidity_str, analogLDRvoltage_str, digitalLuxes_str);

  USB.print(dataToSend);

  USB.print(F("\nTemperature:"));
  USB.print(temperature);
  USB.println(F(" Celsius"));

  USB.print(F("Humidity:"));
  USB.print(humidity);
  USB.println(F(" %"));

  USB.print(F("Atmospheric pressure:"));
  USB.print(pressure);
  USB.println(F(" Pa"));

  USB.print(F("luxes:"));
  USB.println(digitalLuxes);

  USB.print(F("LDR:"));
  USB.println(analogLDRvoltage);

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

