import torch
from torch import no_grad, LongTensor
from fast_vits import commons

from scipy.io.wavfile import write
from fast_vits.models import SynthesizerTrn
from fast_vits import utils
from fast_vits.text import text_to_sequence, _clean_text

device = "cuda:0" if torch.cuda.is_available() else "cpu"
import logging

logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("markdown_it").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

language_marks = {
    "한국어": "[KO]",
    "Japanese": "",
    "日本語": "[JA]",
    "简体中文": "[ZH]",
    "English": "[EN]",
    "Mix": "",
}
lang = ['한국어', '日本語', '简体中文', 'English', 'Mix']

config_dir = "vits_models/configs/config.json"
model_dir = "vits_models/models/G_latest.pth"

hps = utils.get_hparams_from_file(config_dir)
net_g = SynthesizerTrn(
    len(hps.symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model).to(device)
_ = net_g.eval()
_ = utils.load_checkpoint(model_dir, net_g, None)
speaker_ids = hps.speakers


def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def create_tts_fn(model, hps, speaker_ids):
    def tts_fn(text, speaker, speed, language=None, channel_id=None):
        if language is not None:
            text = language_marks[language] + text + language_marks[language]

        speaker_id = speaker_ids[speaker]
        stn_tst = get_text(text, hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = model.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.1, noise_scale_w=0.1,
                                length_scale=1.0 / speed)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid
        ch_path = f"./output/{channel_id}_output.wav"
        write(ch_path, hps.data.sampling_rate, audio)
        return "Success", (hps.data.sampling_rate, audio)

    return tts_fn


tts_fn = create_tts_fn(net_g, hps, speaker_ids)
tts_fn("집에 가고 싶습니다.", "Milk", 1.0, "한국어")
