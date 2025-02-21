import subprocess
from datetime import datetime, timedelta
import json

def copy_folder_to_remote(local_folder, remote_ip, remote_user, remote_path, password):
    """
    指定したフォルダをリモートPCにパスワード認証でコピーする関数。

    :param local_folder: ローカルのフォルダパス（例: "/home/user/data"）
    :param remote_ip: リモートPCのIPアドレス（例: "192.168.1.100"）
    :param remote_user: リモートPCのユーザー名（例: "ubuntu"）
    :param remote_path: リモートPCのコピー先ディレクトリ（例: "/home/ubuntu/backup"）
    :param password: SSHログインのパスワード
    """
    yesterday_time = datetime.now() - timedelta(days=1)
    date = yesterday_time.strftime('%Y%m%d')
    local_folder = local_folder + "/" + date
    scp_command = [
        "sshpass", "-p", password, 
        "scp", "-r", local_folder, 
        f"{remote_user}@{remote_ip}:{remote_path}"
    ]

    try:
        subprocess.run(scp_command, check=True)
        print(f"✅ {local_folder} を {remote_user}@{remote_ip}:{remote_path} にコピー完了！")
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    with open("setting/setting.json")as f:
        setting = json.load(f)
    local_folder = setting["edge"]["save_path"]
    remote_ip = setting["server"]["IP"]
    remote_user = setting["server"]["user"]
    remote_path = setting["server"]["save_path"]
    password = setting["server"]["password"]
    copy_folder_to_remote(local_folder, remote_ip, remote_user, remote_path, password)