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
# 2. Scene 5 分镜英文台词 Mapping
# ---------------------------------------------------------
scene5_scripts = {
    "Shot5-1.mp3": (
        "Finally, what if we double that to a massive 10,000 kcal?"
    ),
    "Shot5-2.mp3": (
        "That huge 11.63 kWh of power can fully charge a modern smartphone "
        "nearly 700 times—powering your daily phone use for almost 2 full years!"
    ),
    "Shot5-3.mp3": (
        "And if you detonated all 10,000 kcal at once as pyrotechnics?"
    ),
    "Shot5-4.mp3": (
        "You'd get a breathtaking, full-scale fireworks show with over "
        "a dozen display shells lighting up the whole sky at once!"
    )
}

# ---------------------------------------------------------
# 3. 异步 TTS 生成函数
# ---------------------------------------------------------
async def generate_audio():
    print(f"🎙️ 开始批量生成 Scene 5 音频文件（保存至: {AUDIO_DIR}）...\n")
    
    for filename, text in scene5_scripts.items():
        output_path = os.path.join(AUDIO_DIR, filename)
        print(f"🔊 正在生成 {filename} ...")
        print(f"   台词: \"{text}\"")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
        print(f"   ✅ 已保存 -> {output_path}\n")
        
    print("🎉 Scene 5 所有音频（Shot5-1 至 Shot5-4）生成完毕！全剧音频大功告成！")

if __name__ == "__main__":
    asyncio.run(generate_audio())
