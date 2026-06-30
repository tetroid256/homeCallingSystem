#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"  // 💡 作成した設定ファイルを読み込む

// ブザー（または内蔵LED）のピン番号
// ※画像から見るとXiao ESP32-C6等の最新ボードのようです。内蔵LEDピンやGPIOピンを指定してください。
const int BUZZER_PIN = D2; 

WiFiClient espClient;
PubSubClient client(espClient);

// Wi-Fi接続関数
void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

// MQTTメッセージ受信時のコールバック関数
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    
    String message = "";
    for (unsigned int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.println(message);

    // メッセージが「RING」ならブザー鳴動（今回は1秒点灯でテスト）
    if (message == "RING") {
        Serial.println("🔔 通知を受信！ブザーを鳴らします。");
        digitalWrite(BUZZER_PIN, HIGH);
        delay(1000);
        digitalWrite(BUZZER_PIN, LOW);
    }
}

// MQTT再接続関数
void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect(MQTT_CLIENT_ID)) {
            Serial.println("connected");
            // config.hで定義したトピックを購読
            client.subscribe(MQTT_TOPIC_NOTICE);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);

    setup_wifi();
    client.setServer(MQTT_SERVER, MQTT_PORT);
    client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop(); // MQTTのポーリング処理
}