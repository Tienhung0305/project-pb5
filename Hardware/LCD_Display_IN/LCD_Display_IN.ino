#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
#define I2C_SDA 15
#define I2C_SCL 14
int number_slot = 0;
int number_now = 0;
int number_slot_max = 6;

const char* ssid = "hileo";
const char* password = "11111111";
const char* serverAddress = "http://192.168.6.94:8000/capture/get_slot";

HTTPClient http;

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);

    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Wire.begin(I2C_SDA, I2C_SCL);
  lcd.init();
  lcd.backlight();
  http.begin(serverAddress);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("...BAI DO XE...");
    lcd.setCursor(0, 1);
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      Serial.println(httpResponseCode);
      if (httpResponseCode == 200) {
        lcd.clear();
        number_slot = http.getString().toInt();
        if (number_slot > number_now) {
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print(".CHAO MUNG BAN!.");

          lcd.setCursor(0, 1);
          lcd.print("SO LUONG: " + String(number_slot) + "/" + String(number_slot_max));
        }
        else
        {
          lcd.setCursor(0, 1);
          lcd.print("SO LUONG: " + String(number_slot) + "/" + String(number_slot_max));
        }
        number_now = number_slot;
      }
    } else {
      Serial.print("Error on HTTP request: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
  delay(2000);
}