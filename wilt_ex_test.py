#環境名はEdgeWilt_env
#source EdgeWilt_env/bin/activateで起動
from main import main

from datetime import datetime, timedelta

start_time = datetime(2025, 2, 8, 7, 0, 0)
end_time = datetime(2025, 2, 8, 17, 0, 0)
interval = 1
id = "test"


for i in range(int((end_time - start_time).total_seconds() / 60)):
    now_time = start_time + timedelta(minutes=i)
    # print(now_time)
    main(id, now_time, 10, False)