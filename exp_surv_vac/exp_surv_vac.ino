/*--------------------------------------------------------------
  Program:      eth_websrv_page

  Description:  Arduino web server that serves up a basic web
                page. Does not use the SD card.
  
  Hardware:     Arduino Uno and official Arduino Ethernet
                shield. Should work with other Arduinos and
                compatible Ethernet shields.
                
  Software:     Developed using Arduino 1.0.3 software
                Should be compatible with Arduino 1.0 +
  
  References:   - WebServer example by David A. Mellis and 
                  modified by Tom Igoe
                - Ethernet library documentation:
                  http://arduino.cc/en/Reference/Ethernet

  Date:         7 January 2013
 
  Author:       W.A. Smith, http://startingelectronics.org

  Edited by:    JP Bureik, LCF, IOGS, 20/09/17
--------------------------------------------------------------*/

#include <SPI.h>
#include <Ethernet.h>

// MAC address from Ethernet shield sticker under board
byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x69, 0x86 };
IPAddress ip(192, 168, 1, 19); // IP address, may need to change depending on network
EthernetServer server(80);  // create a server at port 80

void setup()
{
    Ethernet.begin(mac, ip);  // initialize Ethernet device
    server.begin();           // start to listen for clients
}

void loop()
{
    EthernetClient client = server.available();  // try to get client

    if (client) {  // got client?
        boolean currentLineIsBlank = true;
        while (client.connected()) {
            if (client.available()) {   // client data available to read
                char c = client.read(); // read 1 byte (character) from client
                // last line of client request is blank and ends with \n
                // respond to client only after last line received
                if (c == '\n' && currentLineIsBlank) {
                    // send a standard http response header
                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-Type: text/html");
                    client.println("Connection: close");
                    client.println();
                    // send web page
                    client.println("<!DOCTYPE arduino_due");
                    client.println("<!ELEMENT arduino_due (sensor)*>");
                    client.println("<!ELEMENT sensor (#PCDATA)>");
                    client.println("<!ATTLIST sensor type CDATA #REQUIRED>");
                    client.println("<!ATTLIST sensor reading CDATA #REQUIRED>");
                    client.println("<xml>");
                    client.println("<head>");
                    client.println("<title>Helium 2 Experiment Surveillance</title>");
                    client.println("</head>");
                    client.println("<body>");
                    client.println("<h1>Science chamber vacuum</h1>");
                    client.println("<p>Analog input readings</p>");
                    client.println("<arduino_due>");
                    // output the value of each analog input pin
                    for (int analogChannel = 0; analogChannel < 12; analogChannel++) {
                      int analogPin = analogChannel;
                      int sensorReading = 0;
                      analogReadResolution(12);
                      sensorReading = analogRead(analogPin);
                      client.print("<sensor type = \"analog\">");
                      client.print(analogPin);
                      client.print("</sensor>");

                      client.print(" - ");

                      client.print("<sensor reading>");
                      client.print(sensorReading);
                      client.print("</sensor>");
                                           
                      client.println("<br />");
                    }            
                    client.println("</body>");
                    client.println("</xml>");
                    break;
                }
                // every line of text received from the client ends with \r\n
                if (c == '\n') {
                    // last character on line of received text
                    // starting new line with next character read
                    currentLineIsBlank = true;
                } 
                else if (c != '\r') {
                    // a text character was received from client
                    currentLineIsBlank = false;
                }
            } // end if (client.available())
        } // end while (client.connected())
        delay(1);      // give the web browser time to receive the data
        client.stop(); // close the connection
    } // end if (client)
}
