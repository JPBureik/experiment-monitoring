#include <SPI.h>
#include <Ethernet.h>

byte b = byte(5);

// network configuration.  gateway and subnet are optional.

 // the media access control (ethernet hardware) address for the shield:
byte mac[] = {  0xA8, 0x61, 0x0A, 0xAE, 0x7D, 0x12
};
//the IP address for the shield:
byte ip[] = {10, 117, 53, 45};
// the router's gateway address:
byte gateway[] = { 172, 20, 255, 253};
// the subnet:
byte subnet[] = { 255, 255, 0, 0 };

// telnet defaults to port 23
EthernetServer server = EthernetServer(6574);

void setup()
{
  Serial.begin(9600);

  // start the Ethernet connection without DHCP (with DCHP: Ethernet.begin(mac)):
  //Serial.println("Initialize Ethernet without DHCP:");
  //Ethernet.begin(mac, ip, gateway, subnet);
  Serial.println("Initialize Ethernet with DHCP:");
  Ethernet.begin(mac);
  //Ethernet.setLocalIP(ip);
  Serial.print(" Local IP ");
  Serial.println(Ethernet.localIP());

  // give the Ethernet shield a second to initialize:
  delay(1000);
  // start listening for clients:
  server.begin();
}

void loop()
{
  // if an incoming client connects, there will be bytes available to read:
  EthernetClient client = server.available();
  if (client) {
    Serial.println("Connected client.");
    Serial.println(client.read());
    server.write(b);
    Serial.println("Sent message.");
  }

  
    
  
}
