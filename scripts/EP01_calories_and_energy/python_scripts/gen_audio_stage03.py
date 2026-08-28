import os
import asyncio
import edge_tts

# ---------------------------------------------------------
# 1. 基础配置与路径设置
# ---------------------------------------------------------
BASE_DIR = "/Users/xichen/Desktop/PJ/Social_Media_video/scripts/EP01_calories_and_energy"
AUDIO_DIR = os.path.join(BASE_DIR, "Assets", "audio")

os.makedirs(AUDIO_DIR, exist_ok=True)

# 保持声音角色一致
VOICE = "en-US-AndrewMultilingualNeural"

# ---------------------------------------------------------
# 2. Scene 3 分镜英文台词 Mapping
# ---------------------------------------------------------
scene3_scripts = {
    "Shot3-1.mp3": (
        "Scaling up to our second benchmark: 3,500 kcal."
    ),
    "Shot3-2.mp3": (
        "To understand this energy scientifically, 1,000 grams (1 kg) "
        "of TNT releases about 1,000 kcal upon detonation."
    ),
    "Shot3-3.mp3": (
        "Thus, 3,500 kcal carries the raw chemical energy of 3,500 grams "
        "(3.5 kg) of TNT explosives!"
    ),
    "Shot3-4.mp3": (
        "If released instantly through pyrotechnics, this energy translates "
        "into 2 to 3 massive festival display shells, exploding into temperatures "
        "up to 2,000°C!"
    )
}

# ---------------------------------------------------------
# 3. 异步 TTS 生成函数
# ---------------------------------------------------------
async def generate_audio():
    print(f"🎙️ 开始批量生成 Scene 3 音频文件（保存至: {AUDIO_DIR}）...\n")
    
    for filename, text in scene3_scripts.items():
        output_path = os.path.join(AUDIO_DIR, filename)
        print(f"🔊 正在生成 {filename} ...")
        print(f"   台词: \"{text}\"")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
        print(f"   ✅ 已保存 -> {output_path}\n")
        
    print("🎉 Scene 3 所有音频（Shot3-1 至 Shot3-4）生成完毕！")

if __name__ == "__main__":
    asyncio.run(generate_audio())
