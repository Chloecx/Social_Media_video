import os
from moviepy import VideoFileClip, concatenate_videoclips

# ---------------------------------------------------------
# 1. 基础配置与路径设置
# ---------------------------------------------------------
BASE_DIR = "/Users/xichen/Desktop/PJ/Social_Media_video/scripts/EP01_calories_and_energy"
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
FINAL_OUTPUT_PATH = os.path.join(ASSETS_DIR, "EP01_Full_Video.mp4")

FPS = 30

# 按顺序排列的所有场景输出视频
stage_files = [
    "Stage1_Output.mp4",
    "Stage2_Output.mp4",
    "Stage3_Output.mp4",
    "Stage4_Output.mp4",
    "Stage5_Output.mp4",
    "Stage6_Output.mp4"
]

# ---------------------------------------------------------
# 2. 拼接主逻辑
# ---------------------------------------------------------
clips_to_merge = []

print("🎬 开始读取并直接无缝拼接 Stage 1 至 Stage 6 所有视频...", flush=True)

for stage_name in stage_files:
    stage_path = os.path.join(ASSETS_DIR, stage_name)
    
    if not os.path.exists(stage_path):
        print(f"⚠️ 警告: 未找到 {stage_name}，将跳过该场景！")
        continue

    print(f"  └─ 📥 加载场景: {stage_name}")
    clip = VideoFileClip(stage_path)
    clips_to_merge.append(clip)

# ---------------------------------------------------------
# 3. 导出最终完整视频
# ---------------------------------------------------------
if clips_to_merge:
    print("\n🚀 正在首尾无缝整合全剧视频，开始渲染最终导出文件...", flush=True)
    # 使用 concatenate_videoclips 直接无缝连接（保留每个 Stage 末尾原有的 0.5 秒定格）
    final_video = concatenate_videoclips(clips_to_merge, method="compose")
    
    final_video.write_videofile(
        FINAL_OUTPUT_PATH,
        fps=FPS,
        codec="libx264",
        audio_codec="aac"
    )
    print(f"\n🎉 恭喜！EP01 全剧视频合成完成！文件已保存至：\n👉 {FINAL_OUTPUT_PATH}")
else:
    print("❌ 未找到任何可拼接的场景视频文件，请检查 Assets 目录！")
