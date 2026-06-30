# my_module/mqtt_notifier.py
import paho.mqtt.publish as publish  # 💡 単発送信用のモジュールをインポート
import config

def send_ring_notice():
    """
    指定されたトピックに対して『RING』というメッセージを単発送信する共通関数
    """
    try:
        print(f"[MQTT] トピック {config.MQTT_TOPIC_NOTICE} へ 'RING' を一発送信します...")
        
        # 💡 接続・ループ・送信・切断をこの1行ですべて完璧に処理します
        publish.single(
            topic=config.MQTT_TOPIC_NOTICE,
            payload="RING",
            hostname=config.MQTT_SERVER,
            port=config.MQTT_PORT
        )
        
        return True
    except Exception as e:
        print(f"[MQTT エラー] 送信に失敗しました: {e}")
        return False