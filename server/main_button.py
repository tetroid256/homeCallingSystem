import time
from gpiozero import Button
from signal import pause
from my_module.mqtt_notifier import send_ring_notice

# GPIO 24番ピンをボタン入力として定義（内部プルアップ有効）
BUTTON_PIN = 24
button = Button(BUTTON_PIN, pull_up=False)

def on_button_pressed():
    """
    ボタンが押された瞬間（ポジティブエッジ）に起動するコールバック関数 
    """
    print("\n[入力検知] 物理ボタンが押されました！")
    # 💡 分離した送信関数を呼び出す
    success = send_ring_notice()
    if success:
        print("[処理完了] 通知送信が成功しました。")

def main():
    print(f"--- 物理ボタン監視プログラム起動 (GPIO {BUTTON_PIN}) ---")
    print("ボタンが押されるのを待っています... (終了するには Ctrl+C)")
    
    # 💡 ボタンが押されたとき（pressed）に実行する関数を登録
    button.when_pressed = on_button_pressed
    
    # プログラムが終了しないように待機状態を維持
    pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nプログラムを安全に終了しました。")
    finally:
        button.close()