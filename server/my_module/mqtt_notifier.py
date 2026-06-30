import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import config

def send_ring_notice():
    """
    指定されたトピックに対して『RING』というメッセージを送信する共通関数
    """
    try:
        # MQTTクライアントの初期化
        client = mqtt.Client(CallbackAPIVersion.VERSION2)
        
        # ブローカーに接続
        client.connect(config.MQTT_SERVER, config.MQTT_PORT, 60)
        
        # 呼び出しコマンド「RING」をパブリッシュ
        print(f"[MQTT] トピック {config.MQTT_TOPIC_NOTICE} へ 'RING' を送信します...")
        client.publish(config.MQTT_TOPIC_NOTICE, "RING")
        
        # 接続を綺麗に切断
        client.disconnect()
        return True
    except Exception as e:
        print(f"[MQTT エラー] 送信に失敗しました: {e}")
        return False