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
# 2. Scene 4 分镜英文台词 Mapping
# ---------------------------------------------------------
scene4_scripts = {
    "Shot4-1.mp3": (
        "Moving to 5,000 kcal, what does this massive block of energy "
        "actually represent in biological terms?"
    ),
    "Shot4-2.mp3": (
        "In human biology, one kilogram of pure body fat stores roughly 7,700 kcal."
    ),
    "Shot4-3.mp3": (
        "So 5,000 kcal is scientifically exact to burning about 0.65 kilograms "
        "(1.4 lbs) of pure human fat!"
    ),
    "Shot4-4.mp3": (
        "Converted into household electricity, that fat-burning energy yields 5.81 kWh "
        "— enough to run a 1.5-horsepower air conditioner for nearly 10 solid hours!"
    )
}

# ---------------------------------------------------------
# 3. 异步 TTS 生成函数
# ---------------------------------------------------------
async def generate_audio():
    print(f"🎙️ 开始批量生成 Scene 4 音频文件（保存至: {AUDIO_DIR}）...\n")
    
    for filename, text in scene4_scripts.items():
        output_path = os.path.join(AUDIO_DIR, filename)
        print(f"🔊 正在生成 {filename} ...")
        print(f"   台词: \"{text}\"")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
        print(f"   ✅ 已保存 -> {output_path}\n")
        
    print("🎉 Scene 4 所有音频（Shot4-1 至 Shot4-4）生成完毕！")

if __name__ == "__main__":
    asyncio.run(generate_audio())
