#include <MKRWAN.h> 
LoRaModem modem; 
String appEui = "A8610A32331B7D07"; 
String appKey = "B19FC2B292A6F29FDCAA49D16132E9F9"; 
bool connected; 
int err_count; 
short con;  
void setup() { 
 Serial.begin(115200); 
 while (!Serial); 
 Serial.println("Welcome to MKR WAN 1310 "); 
 modem.begin(US915);

 delay(1000); // apparently the murata dislike if this tempo is removed...  connected=false; 
 err_count=0; 
 con =0; 
} 
void loop() { 
 char msg[2] = {3,4}; 
 short test = 27;  
 if ( !connected ) { 
 Serial.print("Join test : "); 
 Serial.println(++con); 
 int ret=modem.joinOTAA(appEui, appKey); 
 if ( ret ) { 
 connected=true; 
 modem.minPollInterval(60); 
 Serial.println("Connected"); 
 modem.dataRate(5); // switch to SF7 
 delay(100); // more stable 
 err_count=0; 
 } 
 } 
 if ( connected ) { 
 int err=0; 
 modem.beginPacket(); 
 modem.write(msg,2); 
 modem.write(test);  
 modem.print(test); 
 err = modem.endPacket(); 
 if ( err <= 0 ) { 
 Serial.print("Error : "); 
 Serial.println(err); 
 // Confirmation not received - jam or coverage fault 
 err_count++; 
 if ( err_count > 50 ) { 
 connected = false; 
 } 
 // wait for 2min for duty cycle with SF12 - 1.5s frame 
 for ( int i = 0 ; i < 120 ; i++ ) { 
 delay(1000); 
 } 
 } else { 
 err_count = 0; 
 // wait for 20s for duty cycle with SF7 - 55ms frame 
 delay(20000); 
 Serial.println("Message sent");  
 } 
 } 
