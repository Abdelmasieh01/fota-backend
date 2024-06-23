#include <Arduino.h>
#include <LittleFS.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>
#include <Arduino_JSON.h>
#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;

/* 1. Define the WiFi credentials */
#define WIFI_SSID "Orange-F22C" //Orange-F22C //iPhone //WE84A13D
#define WIFI_PASSWORD "3BAQHFY8D45" //3BAQHFY8D45 //11112222 //ka078019



String httpGETRequest(const char* serverName);
void httpGETfile(String FilePath);
void ReadFile(const char* path);
void BootLoader_Send_Data();

String Token = "fde2f99c7c3d73e587e54cb2b12e8c8ed833b209";
const char* serverName = "http://192.168.1.108:8000/latest-car/2/";

char* server = "http://192.168.1.108:8000";
const char* path = "/update.bin";
// http://192.168.1.108:8000/latest-car/2/    version
// 

String payload;
JSONVar version_stm = "1.0";
JSONVar version_back = "0.0"; 



void setup() {

  Serial.begin(115200);
  Serial1.begin(115200);
  // Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
    unsigned long ms = millis();
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(300);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();
}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;
  
    Serial.print("[HTTP] begin...\n");
    payload = httpGETRequest(serverName);
    Serial.println(payload);
    JSONVar latest_firmware = JSON.parse(payload);


    String FilePath = (String)latest_firmware["file"];
    Serial.print("\n");
    Serial.print(FilePath);
    Serial.print("\n");
    httpGETfile(FilePath);
    
    delay(5000);

    Serial.print("..BL..\n");
    BootLoader_Send_Data();

     /*
    version_back = latest_firmware["version"];
    Serial.print("version_back = ");
    Serial.print(version_back);
    Serial.print("\n");
    
    
    if( (String)version_back != (String)version_stm)
    {
      Serial.print("Need version update...\n");
      //get file 

      //send file to STM

      //recive confirm 

      //jump to app in STM
    }
    else
    {
      Serial.print("NO Need...\n");
    }
    
    */
  delay(10000);
}
}

char buffer[2] = {0};
//pakcet without CRC 
char packet[71]; 
/* PACKET LEN (1)
   CMD(1)
   ADDRESS(4)
   DATA LEN(1)
   Data(64)
*/
void BootLoader_Send_Data()
{ 
  LittleFS.begin();
  File file = LittleFS.open("/update.bin","r");
  if (!file.available())
  {
    Serial.print("File Not Avaliable \n");
  }
  while(file.available())
  {
    char count_byte = 0;
    packet[0] = 70; //PACKET LEN
    packet[1] = 0x16;//CMD to write
     //ADDRESS
     //0x8008000
    *(int *) (&packet[2]) = 0x8008000;
    packet[6] = 64; //DATA LEN

    //Serial1.write("Bootloader Start");
    //delay(100);
    //we need to read 64 byte and send it to the bootloader


    while(count_byte < 64)
    {
      file.readBytes(buffer, 2); //binary 

      //binary 45 = 2 byte as string
      // can be stored in 1 byte hexa 
      char HexData = strtol(buffer,NULL,16); //str to long

      //store data in packet
      //7 cause count byte starts at zero
      packet[7 + count_byte] = HexData;

      Serial.printf("packet[%i] = %x \n",7 + count_byte,packet[7 + count_byte]);
      count_byte++;
    }

    //send data 
    int i;
    for (i = 0; i < 7; i++)
    {
      Serial1.write(packet[i]);  //send on uart1
    }
    count_byte = 0;
    while(count_byte < 64)
    { 
      Serial1.write(packet[7 + count_byte]); //send on uart1
      count_byte++;
    }
    while(!Serial.available()) //recive on uart0
    {

    }
    Serial.read();
  }
  //after the whole file got sent we now send the command to jump to app
  packet[0] = 1; //PACKET LEN
  packet[1] = 0x14;//CMD
  packet[2] = 0x14;//CMD
  //send data 
  Serial1.write(packet[0]);  //send on uart1
  Serial1.write(packet[1]);  //send on uart1
  Serial1.write(packet[2]);  //send on uart1
  LittleFS.end();
}



void httpGETfile(String FilePath){
  WiFiClient client;
  HTTPClient http;
  Serial.print("\n");
  Serial.print("[FILE] begin...\n");
  Serial.print("\n");
  String serverPath = (String)server +  FilePath;
  Serial.print(" Server PAth : ");
  Serial.print(serverPath);
  Serial.print("\n");
  // Your IP address with path or Domain name with URL path 
  http.begin(client, serverPath);
  // If you need Node-RED/server authentication, insert user and password below
  http.addHeader("Authorization", "Token fde2f99c7c3d73e587e54cb2b12e8c8ed833b209");
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  if (httpResponseCode>0) {
    Serial.print("FILE Response code: ");
    Serial.println(httpResponseCode);
    //payload = http.getString();

    // get file into the file sys
    auto body = http.getString();
    //Serial.println(payload);
    LittleFS.begin();

    File file = LittleFS.open("/update.bin" , "w");
    size_t bytes_Written = file.write(body.c_str());

    if ( bytes_Written == 0){
      Serial.print("Could not write into the file \n"); 
      return;
    }
    file.close();
    LittleFS.end();
  }
  else {
    Serial.print("FILE Error code: ");
    Serial.println(httpResponseCode);
  }
}

void ReadFile(const char* path){
  Serial.printf("Reading File : %s \n",path);
  LittleFS.begin();
  File file = LittleFS.open(path,"r");
  if(!file)
  {
    Serial.printf("FILE NOT FOUND \n");
    return;
  }
  Serial.print("READING FROM FILE \n");
  while(file.available()) { Serial.write(file.read()); }
  file.close();
  LittleFS.end();
  }





String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your IP address with path or Domain name with URL path 
  http.begin(client, serverName);
  
  // If you need Node-RED/server authentication, insert user and password below
  http.addHeader("Authorization", "Token fde2f99c7c3d73e587e54cb2b12e8c8ed833b209");
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}
