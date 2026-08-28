import os
import asyncio
import edge_tts

# ---------------------------------------------------------
# 1. 基础配置与路径设置
# ---------------------------------------------------------
BASE_DIR = "/Users/xichen/Desktop/PJ/Social_Media_video/scripts/EP01_calories_and_energy"
AUDIO_DIR = os.path.join(BASE_DIR, "Assets", "audio")

os.makedirs(AUDIO_DIR, exist_ok=True)

# 使用指定的声音角色
VOICE = "en-US-AndrewMultilingualNeural"

# ---------------------------------------------------------
# 2. Scene 6 (Shot 6-1) 英文台词 Mapping
# ---------------------------------------------------------
scene6_scripts = {
    "Shot6-1.mp3": (
        "What do you want to see next? Drop your wild ideas in the comments down below! "
        "Don't forget to like and subscribe. See you in the next one. Bye"
    )
}

# ---------------------------------------------------------
# 3. 异步 TTS 生成函数
# ---------------------------------------------------------
async def generate_audio():
    print(f"🎙️ 开始生成 Scene 6 片尾音频（保存至: {AUDIO_DIR}）...\n")
    
    for filename, text in scene6_scripts.items():
        output_path = os.path.join(AUDIO_DIR, filename)
        print(f"🔊 正在生成 {filename} ...")
        print(f"   台词: \"{text}\"")
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
        print(f"   ✅ 已保存 -> {output_path}\n")
        
    print("🎉 Scene 6 片尾音频生成完毕！整部视频的全部 Voiceover 音频素材已齐备！")

if __name__ == "__main__":
    asyncio.run(generate_audio())
