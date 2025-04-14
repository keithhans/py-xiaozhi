import os
import wave
import glob

def merge_wav_files(input_dir, output_file):
    """
    合并指定目录下的所有WAV文件
    
    Args:
        input_dir: 输入目录路径
        output_file: 输出文件路径
    """
    # 获取目录下所有wav文件并按文件名排序
    wav_files = sorted(glob.glob(os.path.join(input_dir, "*.wav")))
    
    if not wav_files:
        print(f"在 {input_dir} 目录下没有找到WAV文件")
        return
    
    # 读取第一个文件来获取参数
    with wave.open(wav_files[0], 'rb') as first_wav:
        params = first_wav.getparams()
    
    # 创建输出文件
    with wave.open(output_file, 'wb') as output_wav:
        output_wav.setparams(params)
        
        # 依次读取并写入每个文件的音频数据
        for wav_file in wav_files:
            with wave.open(wav_file, 'rb') as wav:
                # 确保所有文件参数一致
                if wav.getparams() != params:
                    print(f"警告: {wav_file} 的音频参数与其他文件不一致，跳过此文件")
                    continue
                
                # 读取并写入音频数据
                output_wav.writeframes(wav.readframes(wav.getnframes()))
    
    print(f"合并完成！输出文件: {output_file}")

if __name__ == "__main__":
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='合并WAV文件')
    parser.add_argument('input_dir', help='包含WAV文件的输入目录路径')
    parser.add_argument('output_file', help='合并后的WAV文件输出路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 执行合并
    merge_wav_files(args.input_dir, args.output_file)