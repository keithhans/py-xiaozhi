import pyaudio
import wave
import time
import os
from datetime import datetime

def record_audio(duration=5, sample_rate=16000):
    """
    录制音频并保存为WAV文件
    
    Args:
        duration: 录制时长（秒）
        sample_rate: 采样率（Hz）
    """
    # 音频参数设置
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024

    # 初始化PyAudio
    audio = pyaudio.PyAudio()

    try:
        # 打开音频输入流
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=sample_rate,
            input=True,
            frames_per_buffer=CHUNK
        )

        print(f"开始录音，持续 {duration} 秒...")
        frames = []
        
        # 录制音频
        for i in range(0, int(sample_rate / CHUNK * duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            # 显示进度
            if i % 10 == 0:
                print(f"已录制 {i * CHUNK / sample_rate:.1f} 秒...")

        print("录音完成！正在保存...")

        # 创建保存目录
        save_dir = "recordings"
        os.makedirs(save_dir, exist_ok=True)

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_dir, f"recording_{timestamp}.wav")

        # 保存为WAV文件
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"录音已保存到: {filename}")

    finally:
        # 清理资源
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    record_audio()