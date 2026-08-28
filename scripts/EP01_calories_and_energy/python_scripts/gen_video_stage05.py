import os
import re
import whisper_timestamped as whisper
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# ---------------------------------------------------------
# 1. 基础配置与路径设置
# ---------------------------------------------------------
BASE_DIR = "/Users/xichen/Desktop/PJ/Social_Media_video/scripts/EP01_calories_and_energy"
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
OUTPUT_PATH = os.path.join(ASSETS_DIR, "Stage5_Output.mp4")

VIDEO_SIZE = (1920, 1080)
FPS = 30
SHOT_GAP = 0.5  # 镜头间画面定格缓冲时间 (0.5秒)
VALID_EXTENSIONS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]

# ---------------------------------------------------------
# 2. Scene 5 Shot 与素材 mapping 配置
# ---------------------------------------------------------
shots_data = [
    {
        "shot_id": "Shot5-1",
        "audio_file": "Shot5-1.mp3",
        "frames": ["Shot5-1_01"],
        "auto_align": False
    },
    {
        "shot_id": "Shot5-2",
        "audio_file": "Shot5-2.mp3",
        "frames": ["Shot5-2_01", "Shot5-2_02"],
        "auto_align": True,
        # 从 "powering" (powering your daily phone) 开始为画面 2
        "target_keywords": ["powering"]
    },
    {
        "shot_id": "Shot5-3",
        "audio_file": "Shot5-3.mp3",
        "frames": ["Shot5-3_01"],
        "auto_align": False
    },
    {
        "shot_id": "Shot5-4",
        "audio_file": "Shot5-4.mp3",
        "frames": ["Shot5-4_01", "Shot5-4_02"],
        "auto_align": True,
        # 从 "dozen" (a dozen display shells) 开始为画面 2
        "target_keywords": ["dozen"]
    }
]

# ---------------------------------------------------------
# 3. 辅助函数与 AI 节点抓取
# ---------------------------------------------------------
def find_image_file(base_name, assets_dir):
    for ext in VALID_EXTENSIONS:
        full_path = os.path.join(assets_dir, f"{base_name}{ext}")
        if os.path.exists(full_path):
            return full_path
    return None

def extract_split_timestamp(audio_path, target_keywords, total_duration, whisper_model):
    """提取音频中用于切分画面 1 和画面 2 的精确卡点秒数"""
    print(f"🤖 正在使用 Whisper AI 分析 {os.path.basename(audio_path)} 的卡点时间戳...", flush=True)
    audio = whisper.load_audio(audio_path)
    result = whisper.transcribe(whisper_model, audio, language="en")

    word_timestamps = []
    for segment in result.get("segments", []):
        for word_info in segment.get("words", []):
            clean_word = re.sub(r"[^\w\d]", "", word_info["text"].lower())
            word_timestamps.append({
                "word": clean_word,
                "start": word_info["start"],
                "end": word_info["end"]
            })

    split_time = None
    # 匹配 target_keywords 中的单词发音起点
    for kw in target_keywords:
        kw_clean = str(kw).lower()
        for item in word_timestamps:
            if kw_clean in item["word"] or item["word"] in kw_clean:
                split_time = item["start"]
                print(f"  └─ 🎯 识别到卡点关键字 [{item['word']}]，切图时间点: {split_time:.2f}秒", flush=True)
                break
        if split_time is not None:
            break

    # 计算 2 张图各自的时长，若匹配失败则平分
    if split_time is not None and 0.5 < split_time < (total_duration - 0.5):
        return [split_time, total_duration - split_time]
    else:
        print(f"  └─ ⚠️ 未精准捕抓卡点，默认平分音频时长", flush=True)
        half = total_duration / 2.0
        return [half, half]

# ---------------------------------------------------------
# 4. 主渲染逻辑
# ---------------------------------------------------------
compiled_shot_clips = []
whisper_model = None

print("🎬 开始处理 Scene 5 视频合成...", flush=True)

for shot in shots_data:
    shot_id = shot["shot_id"]
    audio_path = os.path.join(AUDIO_DIR, shot["audio_file"])
    
    if not os.path.exists(audio_path):
        print(f"⚠️ 找不到对应的解说音频文件 {audio_path}，跳过此 Shot。")
        continue

    voice_audio = AudioFileClip(audio_path)
    total_audio_duration = voice_audio.duration
    frame_names = shot["frames"]
    num_frames = len(frame_names)

    # 计算时长
    if shot.get("auto_align", False):
        if whisper_model is None:
            whisper_model = whisper.load_model("tiny", device="cpu")
        durations = extract_split_timestamp(
            audio_path, shot["target_keywords"], total_audio_duration, whisper_model
        )
    else:
        per_frame = total_audio_duration / num_frames
        durations = [per_frame] * num_frames

    # 生成 ImageClip
    frame_clips = []
    for idx, base_name in enumerate(frame_names):
        img_path = find_image_file(base_name, ASSETS_DIR)
        if not img_path:
            print(f"⚠️ 未能找到素材图片 {base_name}，跳过该图。")
            continue
            
        dur = durations[idx] if idx < len(durations) else (total_audio_duration / num_frames)
        
        # 镜头最后一张图片增加 0.5s 停留缓冲
        if idx == num_frames - 1:
            dur += SHOT_GAP
            
        print(f"  └─ Shot [{shot_id}] 素材: {os.path.basename(img_path)} | 显示时长: {dur:.2f}s", flush=True)
        img_clip = ImageClip(img_path).with_duration(dur).resized(VIDEO_SIZE)
        frame_clips.append(img_clip)

    if not frame_clips:
        continue

    shot_visual = concatenate_videoclips(frame_clips)
    shot_composite = shot_visual.with_audio(voice_audio)
    compiled_shot_clips.append(shot_composite)

# ---------------------------------------------------------
# 5. 导出视频
# ---------------------------------------------------------
if compiled_shot_clips:
    final_video = concatenate_videoclips(compiled_shot_clips)
    print(f"🚀 开始渲染 Scene 5 最终视频至: {OUTPUT_PATH}", flush=True)
    final_video.write_videofile(
        OUTPUT_PATH,
        fps=FPS,
        codec="libx264",
        audio_codec="aac"
    )
    print("✅ Scene 5 视频制作完成！输出文件：Stage5_Output.mp4", flush=True)
