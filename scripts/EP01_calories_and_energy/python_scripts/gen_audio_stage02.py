import os
import asyncio
import edge_tts

# ---------------------------------------------------------
# 1. 基础配置与路径设置
# ---------------------------------------------------------
BASE_DIR = "/Users/xichen/Desktop/PJ/Social_Media_video/scripts/EP01_calories_and_energy"
AUDIO_DIR = os.path.join(BASE_DIR, "Assets", "audio")

# 确保音频输出文件夹存在
os.makedirs(AUDIO_DIR, exist_ok=True)

# TTS 声音选择（微软高质量美音男子声音）
VOICE = "en-US-AndrewMultilingualNeural"

# ---------------------------------------------------------
# 2. Scene 2 分镜英文台词 Mapping
# ---------------------------------------------------------
scene2_scripts = {
    "Shot2-1.mp3": (
        "Let's start with our first benchmark: 2,500 kcal, "
        "which equals approximately 2.91 kilowatt-hours of power."
    ),
    "Shot2-2.mp3": (
        "Connected to a standard LED living room light bulb, "
        "that amount can keep it lit continuously for 291 hours "
        "— more than 12 full days without stopping!"
    ),
    "Shot2-3.mp3": (
        "Now let's compare that to petroleum. Gasoline is exceptionally energy-dense, "
        "containing about 31,000 kcal per gallon."
    ),
    "Shot2-4.mp3": (
        "When we convert 2,500 kcal to gasoline, it equals just 0.30 liters "
        "(less liquid than a standard 330ml soda can)."
    ),
    "Shot2-5.mp3": (
        "Dumped into an average passenger fuel tank, this small amount would propel "
        "the vehicle for just 2.5 miles — or roughly 4.0 kilometers."
    )
}

# ---------------------------------------------------------
# 3. 异步 TTS 生成函数
# ---------------------------------------------------------
async def generate_audio():
    print(f"🎙️ 开始批量生成 Scene 2 音频文件（保存至: {AUDIO_DIR}）...\n")
    
    for filename, text in scene2_scripts.items():
        output_path = os.path.join(AUDIO_DIR, filename)
        print(f"🔊 正在生成 {filename} ...")
        print(f"   台词: \"{text}\"")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
        print(f"   ✅ 已保存 -> {output_path}\n")
        
    print("🎉 Scene 2 所有音频（Shot2-1 至 Shot2-5）生成完毕！")

if __name__ == "__main__":
    asyncio.run(generate_audio())
