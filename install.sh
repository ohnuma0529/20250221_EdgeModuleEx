#!/bin/bash

set -e  # エラーが発生したら即終了

echo "セットアップを開始します..."

# 必要ならコメント解除して実行
# sudo apt update && sudo apt upgrade -y

# Git ユーザー設定（必要ならコメント解除）
git config --global user.name "ohnuma0529"
git config --global user.email "onuma.riku.20@shizuoka.ac.jp"

# デスクトップへ移動
cd /home/pi/Desktop

# リポジトリをクローン
if [ ! -d "20250221_EdgeModuleEx" ]; then
    git clone https://github.com/ohnuma0529/20250221_EdgeModuleEx.git
else
    echo "リポジトリは既に存在します。"
fi

# リポジトリフォルダへ移動
cd 20250221_EdgeModuleEx

# 仮想環境を作成 & 有効化
if [ ! -d "EdgeModule" ]; then
    python3 -m venv EdgeModule
fi

source EdgeModule/bin/activate

# 必要なパッケージをインストール
pip install --upgrade pip
pip install -r requirements.txt

# Depth Anything v2をclone
if [ ! -d "./Depth-Anything-V2" ]; then
    git clone https://github.com/DepthAnything/Depth-Anything-V2.git
else
    echo "Depth-Anything-V2 は既に存在します。"
fi

# Depth Anything の重みファイルをダウンロード
DEPTH_MODEL_DIR="./Depth-Anything-V2"
MODEL_URL="https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth"
MODEL_PATH="$DEPTH_MODEL_DIR/depth_anything_v2_vits.pth"

mkdir -p "$DEPTH_MODEL_DIR"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Depth Anything の重みファイルをダウンロード中..."
    wget -O "$MODEL_PATH" "$MODEL_URL"
    echo "ダウンロード完了: $MODEL_PATH"
else
    echo "重みファイルは既に存在します。"
fi

# systemdサービスを設定
cd service
sudo cp calc_wilt.service /etc/systemd/system/
sudo cp calc_wilt.timer /etc/systemd/system/
sudo cp copy_folder.service /etc/systemd/system/
sudo cp copy_folder.timer /etc/systemd/system/
sudo cp cpu_checker.service /etc/systemd/system/

# サービスを有効化
sudo systemctl enable calc_wilt.service
sudo systemctl enable copy_folder.service
sudo systemctl enable cpu_checker.service

# タイマーを開始
sudo systemctl start calc_wilt.timer
sudo systemctl start copy_folder.timer
sudo systemctl start cpu_checker.service

echo "セットアップが完了しました！"
