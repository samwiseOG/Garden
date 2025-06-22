//sensor packages
#include <Wire.h>
#include <Adafruit_SHT4x.h>
#include "Arduino.h"

//server data
#include <WiFiS3.h>
#include <ArduinoJson.h>
#include <ArduinoHttpClient.h>
#include <NTPClient.h> // Include the NTPClient library
#include <WiFiUdp.h> // Include the WiFiUdp library

// WiFi credentials
const char* ssid = "Chance the Router";
const char* password = "getoutofmyhouse";

// Raspberry Pi API info
const char* server = "192.168.50.79"; // Replace with your Pi's IP address
const int port = 5000;
const char* path = "/data";

WiFiClient client;

// Define NTP Client to get time
WiFiUDP ntpUDP; // Create a UDP object
NTPClient timeClient(ntpUDP); // Create an NTPClient object

#define indicatorLight 2

Adafruit_SHT4x sht4 = Adafruit_SHT4x(); // SHT41 object

const int soilMoisturePin = A0; // Analog pin for soil moisture sensor
const byte PHOTORESISTOR_PIN = A1;


void setup() {
  Serial.begin(9600);
  SHT_setup();
  connect();
  timeClient.update();
  int timestamp = timeClient.getEpochTime();
  Serial.println(timestamp);
}

void loop() {
  get_temp_humid();
  delay(10000);

}




void SHT_setup() {
  Serial.println("Adafruit SHT4x test");
  if (! sht4.begin()) {
    Serial.println("Couldn't find SHT4x");
  }
  Serial.println("Found SHT4x sensor");
  Serial.print("Serial number 0x");
  Serial.println(sht4.readSerial(), HEX);

  // You can have 3 different precisions, higher precision takes longer
  sht4.setPrecision(SHT4X_HIGH_PRECISION);
  switch (sht4.getPrecision()) {
     case SHT4X_HIGH_PRECISION: 
       Serial.println("High precision");
       break;
     case SHT4X_MED_PRECISION: 
       Serial.println("Med precision");
       break;
     case SHT4X_LOW_PRECISION: 
       Serial.println("Low precision");
       break;
  }

  sht4.setHeater(SHT4X_NO_HEATER);
  switch (sht4.getHeater()) {
    case SHT4X_NO_HEATER:
      Serial.println("No heater");
      break;
    case SHT4X_HIGH_HEATER_1S:
      Serial.println("High heat for 1 second");
      break;
    case SHT4X_HIGH_HEATER_100MS:
      Serial.println("High heat for 0.1 second");
      break;
    case SHT4X_MED_HEATER_1S:
      Serial.println("Medium heat for 1 second");
      break;
    case SHT4X_MED_HEATER_100MS:
      Serial.println("Medium heat for 0.1 second");
      break;
    case SHT4X_LOW_HEATER_1S:
      Serial.println("Low heat for 1 second");
      break;
    case SHT4X_LOW_HEATER_100MS:
      Serial.println("Low heat for 0.1 second");
      break;
  }

}

void get_temp_humid(){

  sensors_event_t humidity, temp;
  timeClient.update();
  int timestamp = timeClient.getEpochTime();
  sht4.getEvent(&humidity, &temp);  // populate temp and humidity objects with fresh data
  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" degrees C");
  Serial.print("Humidity: ");
  Serial.print(humidity.relative_humidity);
  Serial.println("% rH");
  Serial.print("Read duration (ms): ");
  Serial.println(timestamp);

  send_data(temp.temperature, "temperature",timestamp);
  send_data(humidity.relative_humidity, "humidity",timestamp);
}


void connect(){
  Serial.print("Connecting to WiFi...");
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected!");

}


void send_data(float value, String sensor,unsigned long timestamp){
  if (client.connect(server, port)) {
    Serial.println("Connected to server.");

    // Build JSON payload
    StaticJsonDocument<200> doc;
    doc["time"] = timestamp;
    doc["sensor"] = sensor;
    doc["value"] = value;
    


    String jsonData;
    serializeJson(doc, jsonData);

    // Send HTTP POST request
    client.print(String("POST ") + path + " HTTP/1.1\r\n" +
                 "Host: " + server + "\r\n" +
                 "Content-Type: application/json\r\n" +
                 "Content-Length: " + jsonData.length() + "\r\n" +
                 "Connection: close\r\n\r\n" +
                 jsonData);

    // Read and print the response
    while (client.connected() || client.available()) {
      if (client.available()) {
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
    }

    client.stop();
    Serial.println("Disconnected from server.");
  } else {
    Serial.println("Connection to server failed.");
  }

}
