#include <Arduino.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int botonPin = 4;
const int ledPin = 2;

String inputString = "";
bool newMessage = false;

// Dirección I2C del LCD (ajusta si no muestra nada)
LiquidCrystal_I2C lcd(0x23, 16, 2);

void setup() {
  Serial.begin(115200);
  pinMode(botonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  inputString.reserve(200);

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Listo...");
  delay(1000);
  lcd.clear();
}

void loop() {
  if (digitalRead(botonPin) == LOW) {
    delay(100);
    if (digitalRead(botonPin) == LOW) {

      int cantidad_dedos = random(2, 6);

      lcd.clear();
      lcd.print("Muestra ");
      lcd.print(cantidad_dedos);
      lcd.print(" dedos");

      StaticJsonDocument<100> solicitud;
      solicitud["solicitud"] = "PRUEBA_VIDA";
      solicitud["cantidad_dedos"] = cantidad_dedos;
      serializeJson(solicitud, Serial);
      Serial.println();

      bool respuestaVida = esperarRespuesta();
      if (!respuestaVida) {
        lcd.clear();
        lcd.print("Prueba fallida");
        Serial.println("{\"log\":\"Prueba de vida fallida\"}");
        return;
      }

      lcd.clear();
      lcd.print("Mira de frente");
      lcd.setCursor(0, 1);
      lcd.print("a la camara");

      StaticJsonDocument<100> solicitud2;
      solicitud2["solicitud"] = "PRUEBA_IDENTIFICACION";
      serializeJson(solicitud2, Serial);
      Serial.println();

      bool respuestaId = esperarRespuesta();
      if (respuestaId) {
        digitalWrite(ledPin, HIGH);
        lcd.clear();
        lcd.print("Identif. exitosa");
        Serial.println("{\"log\":\"Identificación exitosa, LED encendido\"}");
      } else {
        digitalWrite(ledPin, LOW);
        lcd.clear();
        lcd.print("Identif. fallida");
        Serial.println("{\"log\":\"Identificación fallida\"}");
      }
    }
  }
}

bool esperarRespuesta() {
  unsigned long start = millis();
  while (millis() - start < 20000) {
    if (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {
        newMessage = true;
      } else {
        inputString += c;
      }
    }

    if (newMessage) {
      StaticJsonDocument<100> doc;
      DeserializationError err = deserializeJson(doc, inputString);
      inputString = "";
      newMessage = false;

      if (!err && doc.containsKey("respuesta")) {
        const char* respuesta = doc["respuesta"];
        return strcmp(respuesta, "True") == 0;
      }
    }
  }
  return false;
}
