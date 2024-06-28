import gtts
import edge_tts

def get_gtts(text, channel_id):
    ch_path = f"output/{channel_id}_output.wav"
    tts = gtts.gTTS(text, lang='ko')
    tts.save(ch_path)

async def get_etts(text, channel_id):
    ch_path = f"output/{channel_id}_output.wav"
    communicate = edge_tts.Communicate(text, "ko-KR-SunHiNeural")
    await communicate.save(ch_path)