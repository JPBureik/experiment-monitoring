// Example 6 - Receiving binary data

const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;

void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
    Serial1.begin(9600);
}

void loop() {
    recvBytesWithStartEndMarkers();
    showNewData();
}

void recvBytesWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    byte endMarker = 0x0A;
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
        Serial.print("Received HEX values -- ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(receivedBytes[n], HEX);
            Serial.print(' ');
        }
        Serial.println();
        newData = false;
    }
}
