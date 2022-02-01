/*
 Experiment Monitoring

 An ethernet server that reads out all analog inputs
 (whether they are connected or not) and writes them
 to connecting clients over TCP/IP.

 The measurement data are 12 bit integers. They are sent
 as two bytes over TCP/IP: 2^8 * byte1 + byte2.

 The Ethernet Shield on the Arduino should preferably be
 connected to an IOGS RJ-45 socket and not one on the
 visitor network so it can bypass DHCP and keep its static
 IP (assigned by the Service Info) and communicate with our
 HeliumServer.

 For control and debugging connect Serial Monitor.

 Ethernet setup:
 * If on IOGS network: Don't use DHCP, static IP
 * If on visitor network: Use DHCP, read out IP via serial

 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 * Any non-connected pins will float so make sure to read
   out the correct ones one the client side.

 created 21 May 2020
 modified 5 Nov 2020
 by JP Bureik
 jan-philipp.bureik@institutoptique.fr
 */
 
#include <SPI.h>
#include <Ethernet.h>
#include <math.h>

int i;
int val = 0;
int msg[2];
int analogPin[12] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11};

// Network configuration:
byte mac[] = {0xA8, 0x61, 0x0A, 0xAE, 0x7D, 0x12};
//the IP address for the shield:
byte ip[] = {10, 117, 53, 45};
// the router's gateway address:
byte gateway[] = {172, 20, 255, 253};
// the subnet:
byte subnet[] = {255, 255, 0, 0 };

// Set matching port on client side:
EthernetServer server = EthernetServer(6574);

void setup()
{
  // Serial com for control and debugging:
  Serial.begin(9600);

  // Make use of maximum precision for Due board:
  analogReadResolution(12);
  
  // Static IP: IOGS network:
  Serial.println("Initialize Ethernet without DHCP:");
  Ethernet.begin(mac, ip, gateway, subnet);
  // DHCP: Visitor network - not recommended:
  //Serial.println("Initialize Ethernet with DHCP:");
  //Ethernet.begin(mac);
  //Ethernet.setLocalIP(ip); // Not usually necessary
  Serial.print(" Local IP ");
  Serial.println(Ethernet.localIP());

  // Ethernet shield initialization time:
  delay(1000);
  
  // Start listening for clients:
  server.begin();
}

void loop()
{
  // Wait for incoming client connections to send the measurement data:
  EthernetClient client = server.available();
  if (client) {
    Serial.println("Connected client.");
    //Serial.println(client.read()); // arbitrary client msg for init

    for (i=0; i<12; i++) {
    //for (i=0; i<1; i++) {
      // Analog voltage measurement:

      /* Measure twice and discard first value in order to correct for
      inaccuracies induced by rapidly switching channels without delay. */
      
      val = analogRead(analogPin[i]); // inaccurate
      delayMicroseconds(50);
      val = analogRead(analogPin[i]); // accurate
  
      // Measurement data: 12-bit int -> send msg as 2^8 * msg[0] + msg[1]
      msg[0] = int(val / pow(2,8));
      msg[1] = val - msg[0] * pow(2,8);
      Serial.println(val);
      Serial.println(msg[0]);
      Serial.println(msg[1]);
  
      // Write to client over TCP/IP:
      server.write(msg[0]);
      server.write(msg[1]);
    }

    // End connection:
    client.stop();
  }  
}
