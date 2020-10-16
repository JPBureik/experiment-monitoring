#include <SPI.h>
#include <Ethernet.h>

// network configuration. dns server, gateway and subnet are optional.

 // the media access control (ethernet hardware) address for the shield:
byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x7D, 0x12 };

// the dns server ip
IPAddress dnServer(172, 20, 255, 253);
// the router's gateway address:
IPAddress gateway(172, 20, 255, 253);
// the subnet:
IPAddress subnet(255, 255, 0, 0);

//the IP address is dependent on your network
IPAddress ip(10, 117, 53, 45);

void setup() {
  Serial.begin(9600);

  // initialize the ethernet device
  Ethernet.begin(mac, ip, dnServer, gateway, subnet);
  //print out the IP address
  Serial.print("IP = ");
  Serial.println(Ethernet.localIP());
}

void loop() {
}
