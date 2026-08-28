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
OUTPUT_PATH = os.path.join(ASSETS_DIR, "Stage1_Output.mp4")

VIDEO_SIZE = (1920, 1080)
FPS = 30
SHOT_GAP = 0.5  # Shot 间画面定格缓冲时间 (0.5秒)
VALID_EXTENSIONS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]

# ---------------------------------------------------------
# 2. Shot 与画面素材配置
# ---------------------------------------------------------
shots_data = [
    {
        "shot_id": "Shot1-1",
        "audio_file": "Shot1-1.mp3",
        "frames": ["Shot1-1_01", "Shot1-1_02"],
        "auto_align": False
    },
    {
        "shot_id": "Shot1-2",
        "audio_file": "Shot1-2.mp3",
        "frames": ["Shot1-2_01"],
        "auto_align": False
    },
    {
        "shot_id": "Shot1-3",
        "audio_file": "Shot1-3.mp3",
        "frames": ["Shot1-3_01"],
        "auto_align": False
    },
    {
        "shot_id": "Shot1-4",
        "audio_file": "Shot1-4.mp3",
        # 加入 Shot1-4_00 画面0；01-04 分别对应四个卡路里数字画面
        "frames": ["Shot1-4_00", "Shot1-4_01", "Shot1-4_02", "Shot1-4_03", "Shot1-4_04"],
        "auto_align": True,
        "keywords": ["2500", "3500", "5000", "10000"]
    },
    {
        "shot_id": "Shot1-5",
        "audio_file": "Shot1-5.mp3",
        "frames": ["Shot1-5_01"],
        "auto_align": False
    }
]

# ---------------------------------------------------------
# 3. 辅助函数
# ---------------------------------------------------------
def find_image_file(base_name, assets_dir):
    for ext in VALID_EXTENSIONS:
        full_path = os.path.join(assets_dir, f"{base_name}{ext}")
        if os.path.exists(full_path):
            return full_path
    return None

def extract_keyword_timestamps(audio_path, keywords, total_duration, whisper_model):
    """利用 Whisper 分析音频，精确定位关键字起止秒数"""
    print(f"🤖 正在使用 Whisper AI 分析 {os.path.basename(audio_path)} 语音时间戳...", flush=True)
    audio = whisper.load_audio(audio_path)
    result = whisper.transcribe(whisper_model, audio, language="en")

    word_timestamps = []
    for segment in result.get("segments", []):
        for word_info in segment.get("words", []):
            clean_word = re.sub(r"[^\w\d]", "", word_info["text"].lower())
            word_timestamps.append({
                "word": clean_word,
                "start": word_info["start"]
            })

    detected_starts = []
    for kw in keywords:
        kw_clean = str(kw).lower()
        matched_time = None
        for item in word_timestamps:
            if kw_clean in item["word"] or item["word"] in kw_clean:
                matched_time = item["start"]
                break
        
        if matched_time is not None:
            detected_starts.append(matched_time)
            print(f"  └─ 🎯 识别到数字 [{kw}] 发音起点: {matched_time:.2f}秒", flush=True)
        else:
            print(f"  └─ ⚠️ 未精准识别到数字 [{kw}]，将使用预估比例区间", flush=True)

    # 时间轴组合：[0.0s (画面0起点), 2500起点(画面1), 3500起点(画面2), 5000起点(画面3), 10000起点(画面4), 音频结束]
    if len(detected_starts) == len(keywords):
        ts = [0.0] + detected_starts + [total_duration]
        durations = [ts[i+1] - ts[i] for i in range(len(ts)-1)]
        return durations
    else:
        # 降级备用逻辑：若个别词未对齐，均分音频时间
        per_frame = total_duration / (len(keywords) + 1)
        return [per_frame] * (len(keywords) + 1)

# ---------------------------------------------------------
# 4. 主渲染逻辑
# ---------------------------------------------------------
compiled_shot_clips = []
whisper_model = None

print("🎬 开始处理视频合成（Shot 1-4 包含画面0及4个 AI 卡点）...", flush=True)

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

    if shot.get("auto_align", False):
        if whisper_model is None:
            whisper_model = whisper.load_model("tiny", device="cpu")
        durations = extract_keyword_timestamps(
            audio_path, shot["keywords"], total_audio_duration, whisper_model
        )
    else:
        per_frame = total_audio_duration / num_frames
        durations = [per_frame] * num_frames

    frame_clips = []
    for idx, base_name in enumerate(frame_names):
        img_path = find_image_file(base_name, ASSETS_DIR)
        if not img_path:
            print(f"⚠️ 未能找到素材图片 {base_name}，跳过该图。")
            continue
            
        dur = durations[idx] if idx < len(durations) else (total_audio_duration / num_frames)
        
        # Shot 最后一张图片额外追加 0.5s 静止定格
        if idx == num_frames - 1:
            dur += SHOT_GAP
            
        print(f"  └─ 匹配素材: {os.path.basename(img_path)} | 显示时长: {dur:.2f}s", flush=True)
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
    print(f"🚀 开始渲染最终视频至: {OUTPUT_PATH}", flush=True)
    final_video.write_videofile(
        OUTPUT_PATH,
        fps=FPS,
        codec="libx264",
        audio_codec="aac"
    )
    print("✅ 视频渲染完成！", flush=True)
