// Example 6 - Receiving binary data

const byte numBytes = 512;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;

void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
    Serial1.begin(9600);
}

void loop() {
    recvBytesWithEndMarker();
}

void recvBytesWithEndMarker() {
    static byte ndx = 0;
    byte endMarker = 0;
    byte rb;
   

    while (Serial1.available() > 0) {
        rb = Serial1.read();

        if (rb != endMarker) {
            receivedBytes[ndx] = rb;
            ndx++;
        }
        else{
            numReceived = ndx;  // save the number for use when printing
            ndx = 0;
            Serial.print("Received values -- ");
            for (byte n = 0; n < numReceived; n++) {
                Serial.print(receivedBytes[n]);
                Serial.print(" - ");
            }
            Serial.println();
        }


    }
}
