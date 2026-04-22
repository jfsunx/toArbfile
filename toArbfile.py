import numpy as np
from pathlib import Path

def toArbfile(data, samplerate, fName):
    # 获取数据长度
    numberofpoints = data.shape[0]

    # 获取极值
    data_min = np.min(data)
    data_max = np.max(data)

    # 计算范围，并防范全0数据的除零风险 (ZeroDivisionError)
    range_value = max(abs(data_min), abs(data_max))
    if range_value == 0:
        # 如果全部为0，直接生成全0的int16数组
        data_conv = np.zeros_like(data, dtype=np.int16)
    else:
        # 转换为 DAC 级别，使用 np.int16 显著降低内存占用
        data_conv = np.round(data * 32767 / range_value).astype(np.int16)

    # 智能处理文件后缀：如果已有 .arb 则不重复添加，如果没有则自动加上
    file_path = Path(fName).with_suffix('.arb')

    # 文件创建与写入
    with open(file_path, 'w') as fid:
        # 使用多行字符串一次性写入文件头，减少 I/O 调用次数
        header = (
            "File Format:1.10\n"
            "Channel Count:1\n"
            "Column Char:TAB\n"
            f"Sample Rate:{samplerate}\n"
            f"High Level:{data_max:.4f}\n"
            f"Low Level:{data_min:.4f}\n"
            'Data Type:"Short"\n'
            'Filter:"OFF"\n'
            f"Data Points:{numberofpoints}\n"
            "Data:\n"
        )
        fid.write(header)

        # 【核心优化】使用 numpy 的批量写入替代 Python 原生 for 循环
        np.savetxt(fid, data_conv, fmt='%d')

if __name__ == '__main__':
    # 示例用法
    fs = 50
    t = np.arange(0, 100, 1/fs)
    x = 5 + 10 * np.sin(1 * 2 * np.pi * t) + np.sin(10 * 2 * np.pi * t)
    
    # 即使传入 'example.arb' 也会被正确处理
    toArbfile(x, fs, 'example')