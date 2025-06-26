#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import os
# import time
# from obswebsocket import obsws, requests
#
#
# def input_minutes():
#     """引导用户输入分钟数"""
#     print("⏱️ 请输入录制时长（分钟）：")
#     while True:
#         try:
#             minutes = float(input("> ").strip())
#             if minutes <= 0:
#                 raise ValueError("时长必须大于0")
#             return minutes * 60  # 转换为秒
#         except ValueError as e:
#             print(f"⚠️ 输入错误: {e}，请重新输入数字")
#
#
# def format_time(seconds):
#     """将秒数格式化为 HH:MM:SS"""
#     mins, secs = divmod(seconds, 60)
#     hrs, mins = divmod(mins, 60)
#     return f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d}"
#
#
# def safe_shutdown():
#     """安全关机（可取消）"""
#     print("\n🖥️ 计算机将在10秒后关机！按 Ctrl+C 取消")
#     try:
#         os.system("shutdown /s /t 10")  # Windows
#         # os.system("shutdown -h now")  # Mac/Linux
#         time.sleep(10)
#     except KeyboardInterrupt:
#         os.system("shutdown /a")  # 取消关机
#         print("❌ 已取消关机")
#
#
# def main():
#     # 获取录制时长（分钟→秒）
#     total_seconds = input_minutes()
#     print(f"\n⏰ 已设置: {format_time(total_seconds)}")
#
#     # 连接OBS
#     try:
#         ws = obsws("localhost", 4455, password="111111")  # 密码参数: password="你的密码"
#         ws.connect()
#         ws.call(requests.StartRecording())
#         print("⏺ 录制已开始")
#
#         # 倒计时
#         start_time = time.time()
#         while True:
#             elapsed = time.time() - start_time
#             remaining = max(0, total_seconds - elapsed)
#             print(f"\r剩余时间: {format_time(remaining)}", end="")
#
#             if remaining <= 0:
#                 break
#             time.sleep(1)
#
#         # 结束录制
#         ws.call(requests.StopRecording())
#         print("\n⏹ 录制已完成")
#
#     except Exception as e:
#         print(f"\n⚠️ 发生错误: {e}")
#     finally:
#         if 'ws' in locals():
#             ws.disconnect()
#         # safe_shutdown()
#
#
# if __name__ == "__main__":
#     main()

import os
import time
from obswebsocket import obsws, requests

# def auto_record(minutes):
#     """全自动录制+关机（无需手动操作）"""
#     try:
#         # 连接OBS（重试3次）
#         for _ in range(3):
#             try:
#                 ws = obsws("localhost", 4455, password="111111")  # ← 修改密码
#                 ws.connect()
#                 break
#             except Exception as e:
#                 print(f"⚠️ 连接失败: {e}")
#                 time.sleep(2)
#         else:
#             raise ConnectionError("无法连接OBS")
#
#         # 自动开始录制
#         ws.call(requests.StartRecording())
#         print(f"⏺ 自动录制已启动 | 时长: {minutes}分钟")
#
#         # 倒计时（分钟→秒）
#         for remaining in range(minutes * 60, 0, -1):
#             mins, secs = divmod(remaining, 60)
#             print(f"\r剩余时间: {mins:02d}:{secs:02d}", end="")
#             time.sleep(1)
#
#         # 自动停止录制
#         ws.call(requests.StopRecording())
#         print("\n⏹ 录制已完成")
#
#     finally:
#         if 'ws' in locals():
#             ws.disconnect()
#         # 自动关机（可取消）
#         # os.system("shutdown /s /t 10")  # Windows
#         # os.system("shutdown -h now")  # Mac/Linux
#
# if __name__ == "__main__":
#     minutes = int(input("请输入录制时长（分钟）: "))  # 仅接受整数
#     auto_record(minutes)
from obswebsocket import obsws, requests as obs_requests
import time
import requests as http_requests
import sys


def check_bilibili_live(room_id):
    """
    检查B站直播间状态
    :param room_id: 直播间ID
    :return: True-直播中 False-未直播
    """
    try:
        url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": f"https://live.bilibili.com/{room_id}"
        }
        response = http_requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 更健壮的API响应检查
        if data.get("code") != 0 or "data" not in data:
            print(f"[API警告] 异常响应: {data}")
            return False

        return data["data"]["live_status"] == 1
    except Exception as e:
        print(f"[B站API错误] {e}")
        return False


def auto_record(max_minutes, room_id):
    """
    自动录制函数
    :param max_minutes: 最大录制时长(分钟)
    :param room_id: 直播间ID
    """
    try:
        # 连接OBS
        print("🔌 正在连接OBS...")
        ws = obsws("localhost", 4455, password="111111")
        ws.connect()
        print("✅ OBS连接成功")

        # 等待直播开始
        print("⏳ 等待直播开始...")
        start_time = time.time()
        while not check_bilibili_live(room_id):
            if time.time() - start_time > 300:  # 5分钟超时
                print("❌ 直播未开始，退出脚本")
                return
            time.sleep(30)
            print("\r检测中...", end="", flush=True)

        # 开始录制
        print("\n⏺ 正在启动录制...")
        ws.call(obs_requests.StartRecord())
        print("✅ 录制已启动 | 实时监控中")

        # 主循环
        start_time = time.time()
        max_duration = max_minutes * 60
        failed_checks = 0
        last_check_time = 0  # 上次检测时间

        while True:
            current_time = time.time()
            elapsed = current_time - start_time

            # 每60秒检测一次直播状态
            if elapsed - last_check_time >= 60:
                last_check_time = elapsed
                if not check_bilibili_live(room_id):
                    failed_checks += 1
                    if failed_checks >= 3:  # 连续3次失败才判定停播
                        print("\n❌ 直播已结束，停止录制")
                        break
                else:
                    failed_checks = 0  # 重置计数器

            # 显示剩余时间
            remaining = max(0, int(max_duration - elapsed))
            mins, secs = divmod(remaining, 60)
            print(f"\r剩余时间: {mins:02d}:{secs:02d} | 状态: 直播中", end="", flush=True)

            if remaining <= 0:
                print("\n⌛ 录制时长已达上限")
                break

            time.sleep(1)

        # 停止录制
        print("\n⏹ 正在停止录制...")
        ws.call(obs_requests.StopRecord())
        print("✅ 录制已停止")

    except KeyboardInterrupt:
        print("\n🛑 用户手动中断")
    except Exception as e:
        print(f"\n❌ [脚本错误] {e}", file=sys.stderr)
    finally:
        if 'ws' in locals():
            print("🔌 正在断开OBS连接...")
            ws.disconnect()
            print("✅ OBS连接已断开")


if __name__ == "__main__":
    try:
        print("🎬 B站直播自动录制脚本")
        print("------------------------")
        room_id = input("请输入B站直播间ID(默认1616): ") or "1616"
        minutes = float(input("请输入最大录制时长(分钟): "))

        print("\n⚠️ 注意事项:")
        print("1. 请确保OBS已开启WebSocket服务")
        print("2. 请确保OBS密码正确")
        print("3. 按Ctrl+C可手动终止脚本")
        print("------------------------")

        auto_record(minutes, int(room_id))
    except ValueError:
        print("❌ 错误: 请输入有效的数字", file=sys.stderr)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
    finally:
        print("\n脚本运行结束")