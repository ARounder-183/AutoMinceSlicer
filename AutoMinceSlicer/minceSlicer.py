import os.path
from pathlib import Path
import textgrid
import glob
from pydub import AudioSegment
name = input('请输入segements文件夹下存放wav的文件夹名称：')

wavDir = '.\\segments\\' + name + '\\'
print('wav存放的文件夹为：' + wavDir)
outPath = '.\\Mince\\'
if Path(outPath).exists():
    print('输出文件夹已存在：' + outPath)
else:
    os.makedirs(outPath)
    print('已创建臊子输出的文件夹：' + outPath)
tgDir = '.\\segments\\' + name + '\\TextGrid\\'
print('TextGrid读取的文件夹为：' + tgDir)

if Path(tgDir).exists() == 0:
    print("\n!!!无法找到TextGrid文件，请检查文件路径!!!\n")
for tgPath in glob.glob(os.path.join(tgDir, '*')):
    tg = textgrid.TextGrid()
    tg.read(tgPath)
    tgFileName = os.path.basename(tgPath)
    print("读取文件:" + tgFileName)
    tgNumber = tgFileName.split('_')[1].split('.')[0]
    tgName = tgFileName.split('_')[0]
    wavPath = wavDir + tgName + '_' + tgNumber + '.wav'
    # 切割
    sound = AudioSegment.from_wav(wavPath)
    i = 0
    for j in range(len(tg.tiers[i])):
        start = int(tg.tiers[i][j].minTime * 1000)
        end = int(tg.tiers[i][j].maxTime * 1000)
        cut_wav = sound[start: end]
        outWavPath = outPath + tg.tiers[i][j].mark + '.wav'
        if end - start > 200:
            if os.path.exists(outWavPath):
                suffix = 1
                while os.path.exists(f"{outPath}{tg.tiers[i][j].mark}{suffix}.wav"):
                    suffix += 1
                outWavPath = f"{outPath}{tg.tiers[i][j].mark}{suffix}.wav"
            cut_wav.export(outWavPath, format='wav')
            print('已成功输出文件:' + os.path.basename(outWavPath))

input("已结束，按任意键继续")
