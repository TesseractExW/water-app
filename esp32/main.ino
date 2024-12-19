#include <WiFi.h>
const char **wifi = { "ssid" , "passwword" };
const int pins[] = { 35 , 32 };
const char *url = "https://something:3000/updatesensor";
void setup()
{
    Serial.begin(115200);
    delay(1000);
    WiFi.begin(wifi[0], wifi[1]);
    Serial.println("\nConnecting");
    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(500);
    }
    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
}
void loop()
{
    float tols[2];
    for(x=0; x<10 ; x++)
    {
        for (int i = 0;i < 2;i++) tols[i] += analogRead(pins[i]);
        delay(10);
    }
    float voltages[] =  { tols[0] / 10 * (5.0 / 1023.0),tols[1] / 10 * (5.0 / 1023.0) };
    float ph = voltages[0] * (-6.80) + 25.85;
    float tds = (133.42*pow(voltages[1],3) - 255.86*pow(voltages[1],2) + 857.39 * voltages[1])*0.5;
    if(WiFi.status()== WL_CONNECTED){
        WiFiClient client;
        HTTPClient http;
        http.begin(client, url);
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");
        String httpRequestData = String("id=0&tds=")+String(ph) + String("&ph=") + String(tds);
        int httpResponseCode = http.POST(httpRequestData);
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        
        // Free resources
        http.end();
    }
}