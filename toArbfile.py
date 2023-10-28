import numpy as np


def toArbfile(data, samplerate, fName):

    # Number of points in the data
    numberofpoints = data.shape[0]

    # Get max and min values from waveform data
    data_min = np.min(data)
    data_max = np.max(data)

    # Range has to be the maximum absolute value between data_min and data_max
    range_value = max(abs(data_min), abs(data_max))

    # Data Conversion from V to DAC levels
    data_conv = np.round(data * 32767 / range_value).astype(int)

    fName = fName + '.arb'  # Add file extension to the file name

    # File creation and formatting
    with open(fName, 'w') as fid:
        fid.write('File Format:1.10\n')
        fid.write('Channel Count:1\n')
        fid.write('Column Char:TAB\n')
        fid.write(f'Sample Rate:{samplerate}\n')
        fid.write(f'High Level:{data_max:.4f}\n')
        fid.write(f'Low Level:{data_min:.4f}\n')
        fid.write('Data Type:"Short"\n')
        fid.write('Filter:"OFF"\n')
        fid.write(f'Data Points:{numberofpoints}\n')
        fid.write('Data:\n')

        # Write data to file and close it
        for value in data_conv:
            fid.write(f'{value}\n')


if __name__ == '__main__':
    # Example usage
    fs = 50
    t = np.arange(0, 100, 1/fs)
    x = 5 + 10 * np.sin(1 * 2 * np.pi * t) + np.sin(10 * 2 * np.pi * t)
    samplerate = fs
    fName = 'example'
    toArbfile(x, samplerate, fName)
