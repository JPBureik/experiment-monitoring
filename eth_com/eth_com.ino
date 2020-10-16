#include <SPI.h>
#include <Ethernet.h>

int msg[4];

// network configuration.  gateway and subnet are optional.

 // the media access control (ethernet hardware) address for the shield:
byte mac[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x7D, 0x12 };
//the IP address for the shield:
byte ip[] = {172, 20, 217, 9};
// the router's gateway address:
byte gateway[] = { 172, 20, 255, 253};
// the subnet:
byte subnet[] = { 255, 255, 0, 0 };

// telnet defaults to port 23
EthernetServer server = EthernetServer(23);

void setup()
{
  Serial.begin(9600);
  // initialize the ethernet device:
  Ethernet.begin(mac, ip, gateway, subnet);
  // start listening for clients:
  server.begin();
}

void loop()
{
  // if an incoming client connects, there will be bytes available to read:
  EthernetClient client = server.available();
  if (client) {
    int i ;
    int number_of_bytes = 4;
  for(i=0;i<number_of_bytes;i++){
    msg[i] = client.read();
    Serial.print(msg[i]);
  }

  
    
  }
}
