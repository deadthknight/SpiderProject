import time
import os
from obswebsocket import obsws, requests as obs_requests
import requests as http_requests
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger

logger.add("record_log_{time}.log", format="{time} {level} {message}", level="INFO", rotation="1 week")

def create_browser():
    co = ChromiumOptions()
    co.headless(False)
    co.incognito(True)
    co.set_argument('--start-maximized')
    co.set_argument('--autoplay-policy=no-user-gesture-required')
    return ChromiumPage(co)

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
        live_status = data.get("data", {}).get("live_status", 0)
        return live_status == 1
    except Exception as e:
        logger.error(f"[B站API错误] {e}")
        return False

def shutdown_system():
    logger.info("💻 正在关机...")
    if os.name == 'nt':
        os.system("shutdown /s /t 10")
    else:
        os.system("shutdown -h now")

def wait_until_live(room_id):
    logger.info("⏳ 开始轮询检查直播状态（每10分钟检查一次）")
    while True:
        if check_bilibili_live(room_id):
            logger.info("✅ 直播已开始！准备启动录制流程")
            return
        logger.info("🔁 直播未开始，10分钟后再次检查...")
        time.sleep(600)

def auto_record(max_minutes, room_id):
    ws = None
    page = None
    try:
        # 打开直播网页
        page = create_browser()
        logger.info("🧭 正在打开直播页面...")
        page.get(f"https://live.bilibili.com/{room_id}?")

        # 连接 OBS
        ws = obsws("localhost", 4455, password="111111")
        try:
            ws.connect()
        except Exception as e:
            logger.error(f"[OBS连接失败] {e}，请确认 OBS 已启动并开启 obs-websocket 插件")
            return False

        # 启动录制
        ws.call(obs_requests.StartRecord())
        start_time = time.time()
        logger.info(f"⏺ {time.strftime('%H:%M:%S')} 录制已启动")

        max_duration = max_minutes * 60
        failed_checks = 0
        last_check = 0

        while True:
            now = time.time()
            elapsed = now - start_time
            remaining = max(0, int(max_duration - elapsed))
            mins, secs = divmod(remaining, 60)
            print(f"\r剩余时间: {mins:02d}:{secs:02d} | 状态: 直播中", end="")

            # 每60秒检查一次是否还在直播
            if now - last_check >= 60:
                last_check = now
                if not check_bilibili_live(room_id):
                    failed_checks += 1
                    logger.warning(f"\n⚠️ 直播检测失败次数: {failed_checks}/3")
                    if failed_checks >= 3:
                        logger.warning("❌ 直播已结束，停止录制")
                        break
                else:
                    failed_checks = 0

            if elapsed >= max_duration:
                logger.info("⌛ 达到最大录制时长，准备停止录制")
                break

            time.sleep(1)

        # 停止录制
        ws.call(obs_requests.StopRecord())
        logger.info(f"⏹ {time.strftime('%H:%M:%S')} 录制已停止")
        return True

    except Exception as e:
        logger.error(f"[脚本错误] {e}")
        return False
    finally:
        if ws:
            ws.disconnect()
        if page:
            page.close()

if __name__ == "__main__":
    room_id = 1616
    max_minutes = 300

    # 第一步：先不断检测直播是否已开始
    wait_until_live(room_id)

    # 第二步：直播开始后，打开页面并启动录制
    success = auto_record(max_minutes, room_id)

    # 第三步：录制成功后关机
    if success:
        shutdown_system()
