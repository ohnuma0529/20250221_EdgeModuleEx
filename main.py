from util import read_csv, save_csv
from image_processor import image_processor, capture_image
from influxdb import InfluxDBWrapper

import os
import time
from datetime import datetime
import json

def main():
    # 設定読み込み
    with open("setting/setting.json")as f:
        setting = json.load(f)
    edge_id = setting["edge"]["ID"]
    tracking_num = setting["edge"]["tracking_num"]
    server_flag = setting["edge"]["server_flag"]
    width = setting["edge"]["width"]
    height = setting["edge"]["height"]

    # 撮影前準備
    now_time = datetime.now().replace(second=0, microsecond=0)
    start_time = datetime.strptime(setting["edge"]["start_time"], "%H%M").time()
    end_time = datetime.strptime(setting["edge"]["end_time"], "%H%M").time()
    start_datetime = datetime.combine(datetime.today().date(), start_time)
    end_datetime = datetime.combine(datetime.today().date(), end_time)
    
    date = now_time.strftime('%Y%m%d')
    source_dir = "data/" + date
    os.makedirs(source_dir, exist_ok=True)
    csv_path = os.path.join(source_dir, "result.csv")
    image_dir = os.path.join(source_dir, "images")
    os.makedirs(image_dir, exist_ok=True)

    # 撮影＆保存
    image_path = capture_image(edge_id, now_time, image_dir, (width, height))

    if start_datetime <= now_time <= end_datetime:    
        # ベンチマーク用の時刻取得
        start_time = time.time()

        # csv読込
        df = read_csv(csv_path)

        # その日の初回画像であったり，再検出フラグ列が1だったら初回処理
        img_pro = image_processor(edge_id, df, image_dir, tracking_num, now_time, server_flag)

        if df.empty:
            print("df is empty")
            df = img_pro.first_detection()
        elif 're_detection' not in df.columns:
            print("re_detection is not in df.columns")
            df = img_pro.first_detection()
        elif df['re_detection'].iloc[-1] == 1:
            print("re_detection is 1")
            df = img_pro.first_detection()
        else:
            print("tracking")
            df = img_pro.tracking()

        # csv保存・更新
        save_csv(df, csv_path)

        # 時刻を取得
        end_time = time.time()
        inference_time = end_time - start_time

        # 制御部のInfluxDBにアップロード部分は制御部のDBができてから作成する
        # dfのfinal_wiltの最新の値，inference_timeをnow_timeでアップロードする
        # measurementはid(str)，fieldはwiltとinference_time
        infdb = InfluxDBWrapper("HappyAI")
        infdb.write_single_point(edge_id, now_time, "wilt", float(df['final_wilt'].iloc[-1]))
        infdb.write_single_point(edge_id, now_time, "inference_time", inference_time)

        infdb_server = InfluxDBWrapper("HappyAIServer")
        infdb_server.write_single_point(edge_id, now_time, "wilt", float(df['final_wilt'].iloc[-1]))
        infdb_server.write_single_point(edge_id, now_time, "inference_time", inference_time)
    else:
        print("動作時間外：",now_time)
if __name__ == "__main__":
    main()