import os
import cv2
import pandas as pd
import re
from datetime import datetime, timedelta

def vis_csv(edge_id, timestamp):
    source_dir = "data/" + timestamp.strftime('%Y%m%d')
    datetime_str = timestamp.strftime(f'{edge_id}_%Y%m%d_%H%M')
    image_path = os.path.join(source_dir, "images", f'{datetime_str}.jpg')
    csv_path = os.path.join(source_dir, 'result.csv')

    # 画像の読み込み
    print(image_path)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (1024,1024))
    df = pd.read_csv(csv_path, index_col=0)
    df.index = pd.to_datetime(df.index)
    # timestampの行を取得
    row = df.loc[timestamp]
    # 1_bbox_x1, 1_bbox_y1, 1_bbox_x2, 1_bbox_y2, 2_bbox_x1, 2_bbox_y1, 2_bbox_x2, 2_bbox_y2, 3_bbox_x1, 3_bbox_y1, 3_bbox_x2, 3_bbox_y2
    # 列名の最初の数字がbboxの番号
    # bbox番号の最大値を取得
    max_bbox = max([int(re.match(r'\d+', col).group()) for col in df.columns if re.match(r'\d+', col)])
    print("all_leaf:", max_bbox)
    for i in range(1, max_bbox+1):
        # bboxの描画
        try:
            x1 = int(row[f'{i}_bbox_x1'])
            y1 = int(row[f'{i}_bbox_y1'])
            x2 = int(row[f'{i}_bbox_x2'])
            y2 = int(row[f'{i}_bbox_y2'])
        except:
            print("skip:", i)
            continue
        # bboxの左上にbbox番号を描画
        cv2.putText(image, f'{i}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # Keypointの描画
        # 二つのKeypointを結ぶ線を描画
        try:
            base_x = int(row[f'{i}_base_x'])
            base_y = int(row[f'{i}_base_y'])
            tip_x = int(row[f'{i}_tip_x'])
            tip_y = int(row[f'{i}_tip_y'])
        except:
            continue
        cv2.circle(image, (base_x, base_y), 5, (255, 0, 0), -1)
        cv2.circle(image, (tip_x, tip_y), 5, (0, 0, 255), -1)
        cv2.line(image, (base_x, base_y), (tip_x, tip_y), (0, 255, 0), 2)
        print(base_x, tip_x)
        print(base_y, tip_y)
    #保存
    save_dir = "vis_" + source_dir
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'{datetime_str}.jpg')
    # cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return image

if __name__ == "__main__":
    now_time = datetime(2025, 2, 20, 1, 17, 0)
    vis_csv("test",now_time)