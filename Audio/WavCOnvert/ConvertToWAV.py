from os import path
from pydub import AudioSegment
import glob
import subprocess

def substring_after(s, delim):
    return s.partition(delim)[2]
def substring_before(s,extenstion):
    return s.partition(extenstion)[0]
# sudo apt-get install libsox-fmt-mp3
filenames = glob.glob('/home/luvitusmaximus/Documents/ASR/SampleAudioFiles/'+'*.mp3')
#print(filenames)
# Extract the names of the files.
directory = '/home/luvitusmaximus/Documents/ASR/SampleAudioFiles/WAVFiles/'
mp3names = []
newNames = []
delimiter = '/home/luvitusmaximus/Documents/ASR/SampleAudioFiles/'
for file in filenames:
    name = substring_after(file,delimiter)
    mp3names.append(name)
    name = substring_before(name,'.mp3')
    n = name.split(' ')
    name = n[0]+'_'+ n[1] + '_' + n[2]
    print(name)
    newNames.append(name)
print(newNames)
''' Running the SOX command for all files. '''
i = 0
for file in filenames:
    print('Converting File :',file,'\n')
    subprocess.run(["sox",file,'-c 1','-r 32000',(directory+newNames[i]+'.wav')])
    i = i + 1
