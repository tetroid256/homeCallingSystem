import time
import paho.mqtt.client as mqtt

# 【設定】ラズパイ自身のIP（localhostでも可）
MQTT_SERVER = "localhost" 
MQTT_TOPIC = "house/room1/notice"

def main():
    # MQTTクライアントの初期化
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    print(f"MQTTブローカー（{MQTT_SERVER}）に接続中...")
    client.connect(MQTT_SERVER, 1883, 60)
    
    # ループを開始
    client.loop_start()
    
    try:
        print("テスト送信を開始します。Ctrl+Cで終了します。")
        while True:
            print(f"トピック [{MQTT_TOPIC}] に 'RING' を送信します...")
            # メッセージのパブリッシュ（配信）
            client.publish(MQTT_TOPIC, "RING")
            
            # 5秒ごとに繰り返し送信
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n終了処理中...")
        client.loop_stop()
        client.disconnect()
        print("停止しました。")

if __name__ == "__main__":
    main()