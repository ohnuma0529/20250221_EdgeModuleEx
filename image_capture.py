import cv2
import os
from datetime import datetime

def capture_image(save_folder: str, resolution: tuple):
    # 保存先フォルダが存在しない場合は作成
    os.makedirs(save_folder, exist_ok=True)

    # Webカメラを初期化（0は通常、最初に見つかったカメラを指す）
    cap = cv2.VideoCapture(0)

    # 解像度を設定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # カメラが正しく開けたか確認
    if not cap.isOpened():
        print("カメラを開けませんでした。")
        return

    # フレームをキャプチャ
    ret, frame = cap.read()

    if ret:
        # 保存するファイル名を作成（タイムスタンプ付き）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_folder, f"image_{timestamp}.jpg")

        # 画像を保存
        cv2.imwrite(filename, frame)
        print(f"画像を保存しました: {filename}")
    else:
        print("画像のキャプチャに失敗しました。")

    # カメラを解放
    cap.release()

# 例: 640x480 解像度で 'images' フォルダに保存
# capture_image('images', (640, 480))

if __name__ == '__main__':
    capture_image('images', (640, 480))