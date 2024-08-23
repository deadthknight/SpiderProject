from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job_function():
    print(f"任务运行时间：{datetime.now()}")

# 创建调度器
scheduler = BlockingScheduler()

# 添加任务：每隔10秒运行一次
scheduler.add_job(job_function, 'interval', seconds=10)

# 开始调度
scheduler.start()
