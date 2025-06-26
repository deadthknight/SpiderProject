import time
import os
from obswebsocket import obsws, requests as obs_requests
import requests as http_requests
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger


co = ChromiumOptions()
co.headless(False)  # 无头模式
co.incognito(True)  # 无痕模式

co.set_argument('--start-maximized')   #窗口最大化
# co.mute(True)    # 静音
# co.no_imgs(True) 验证码也加载不了
page = ChromiumPage(co)
logger.info('==========================打开网页=================================')
# 打开网站并登录
page.get('https://live.bilibili.com/1616?')

def check_bilibili_live(room_id):
    try:
        url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://live.bilibili.com/{room_id}"
        }
        response = http_requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["data"]["live_status"] == 1
    except Exception as e:
        print(f"[B站API错误] {e}")
        return False

def shutdown_system():
    print("💻 正在关机...")
    if os.name == 'nt':  # Windows
        os.system("shutdown /s /t 10")
    else:  # macOS 或 Linux
        os.system("shutdown -h now")

def auto_record(max_minutes, room_id):
    try:
        # 连接OBS
        ws = obsws("localhost", 4455, password="111111")
        try:
            ws.connect()
        except Exception as e:
            print(f"[OBS连接失败] {e}")
            return

        # 等待直播开始
        print("⏳ 等待直播开始...")
        start_wait = time.time()
        while not check_bilibili_live(room_id):
            if time.time() - start_wait > 300:
                print("❌ 直播未开始，退出脚本")
                return
            print("\r检测中...", end="")
            time.sleep(30)

        # 开始录制
        ws.call(obs_requests.StartRecord())
        start_time = time.time()
        print(f"\n⏺ {time.strftime('%H:%M:%S')} 录制已启动")

        max_duration = max_minutes * 60
        failed_checks = 0
        last_check = 0

        while True:
            now = time.time()
            elapsed = now - start_time
            remaining = max(0, int(max_duration - elapsed))
            mins, secs = divmod(remaining, 60)
            print(f"\r剩余时间: {mins:02d}:{secs:02d} | 状态: 直播中", end="")

            # 定期检测直播状态（每60秒）
            if now - last_check >= 60:
                last_check = now
                if not check_bilibili_live(room_id):
                    failed_checks += 1
                    print(f"\n⚠️ 检测失败次数: {failed_checks}/3")
                    if failed_checks >= 3:
                        print("\n❌ 直播已结束，停止录制")
                        break
                else:
                    failed_checks = 0

            if elapsed >= max_duration:
                print("\n⌛ 达到最大录制时长，停止录制")
                break

            time.sleep(1)

        # 停止录制
        ws.call(obs_requests.StopRecord())
        print(f"\n⏹ {time.strftime('%H:%M:%S')} 录制已停止")

    except Exception as e:
        print(f"[脚本错误] {e}")
    finally:
        if 'ws' in locals():
            ws.disconnect()
        shutdown_system()

if __name__ == "__main__":
    room_id = 1616  # 替换为你的直播间 ID
    # minutes = float(input("请输入最大录制时长（分钟）: "))
    auto_record(300, room_id)
