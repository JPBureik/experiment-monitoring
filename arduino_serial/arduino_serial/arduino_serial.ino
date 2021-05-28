// Example 6 - Receiving binary data

const byte numBytes = 64;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;

void setup() {
    Serial.begin(19200);
    Serial.println("<Arduino is ready>");
    Serial1.begin(19200);
}

void loop() {
    recvBytesWithStartEndMarkers();
    showNewData();
}

void recvBytesWithStartEndMarkers() {
    static byte ndx = 0;
    byte endMarker = '\n';//0x0A;
    byte rb;
   

    while (Serial1.available() > 0 && newData == false) {
        rb = Serial1.read();

        if (rb != endMarker) {
            receivedBytes[ndx] = rb;
            ndx++;
            if (ndx >= numBytes) {
                ndx = numBytes - 1;
            }
            else {
              receivedBytes[ndx] = '\0'; // terminate the string
              numReceived = ndx;  // save the number for use when printing
              ndx = 0;
              newData = true;
            }
        }


    }
}

void showNewData() {
    if (newData == true) {
        unsigned char hexValue[2];
        Serial.print("Received HEX values -- ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(receivedBytes[n], HEX);
            Serial.print(' ');         
        }
        Serial.println();
        newData = false;
    }
}
