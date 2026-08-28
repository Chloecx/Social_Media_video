import os
import asyncio
import edge_tts

# 1. 基础路径配置
BASE_DIR = "/Users/xichen/Desktop/PJ/Social_Media_video/scripts/EP01_calories_and_energy"
AUDIO_DIR = os.path.join(BASE_DIR, "Assets", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# 2. 每一镜头的英文解说文本
scripts = {
    "Shot1-1": "How far could the chemical energy in food actually drive a 2-ton gasoline car?",
    "Shot1-2": "In physics, a Calorie is not just a nutritional concept; it's strictly a unit of heat energy.",
    "Shot1-3": "One kilocalorie represents the heat required to raise the temperature of 1 kilogram of water by 1 degree Celsius.",
    "Shot1-4": "To see how this translates into actual motion, let's examine four specific benchmarks: 2,500 kcal, 3,500 kcal, 5,000 kcal, and an extreme 10,000 kcal.",
    "Shot1-5": "We will convert each directly into electric energy and fuel equivalents, revealing the mind-bending difference between human metabolism and internal combustion engines."
}

# TTS 声音选择（微软高质量美音男子声音）
VOICE = "en-US-AndrewMultilingualNeural"

async def generate_speech():
    print("🎙️ 开始生成高质量英文解说音频...")
    for shot_id, text in scripts.items():
        output_mp3 = os.path.join(AUDIO_DIR, f"{shot_id}.mp3")
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_mp3)
        print(f"✅ 已生成配音: {output_mp3}")
    print("🎉 所有解说音频（Shot1-1 至 Shot1-5）已成功生成！")

if __name__ == "__main__":
    asyncio.run(generate_speech())
