import wget
'''
<audio src="http://newsonair.nic.in/writereaddata/Bulletins_Audio/Regional/2020/Nov/Regional-Chandigarh-Hindi-1810-2020111820417.mp3" id="ctl00_ContentPlaceHolder1_RepterDetails_ctl00_audio_player" preload="auto" controls="controls" style="width:250px;"></audio>
'''
url = 'http://newsonair.nic.in/writereaddata/Bulletins_Audio/Regional/2020/Nov/Regional-Chandigarh-Hindi-1810-2020111820417.mp3'
name = '/home/luvitusmaximus/Documents/ASR/Audio/DehradunTest.mp3'
print('Downloading :\n')
wget.download(url,name)
print('Downloaded: ')