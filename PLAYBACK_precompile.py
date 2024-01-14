from pyboy import PyBoy
import time
import mido
from mido import MidiFile


debug=False

song=[
    ['C-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['D-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['E-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['F-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['G-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['A-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['B-4 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ['C-5 15 0 1 0 ---','--- 15 0 1 0 ---','---','---',170],
    ]


with open('youkoso.txt','r') as f:
    vg_=f.readlines()
vgmdata=[]
latch=False
for i in vg_:
    if latch: vgmdata.append(i.strip('\r\n'))
    if 'VGMData' in i: latch=True


songframes=[[]]

for i in vgmdata:
    cmd=i[12:14]
    reg=i[15:17]
    val=i[18:20]
    if cmd=='62':
        songframes.append([])
    else:
        songframes[-1].append(i)
    #print('\n'.join([str(yeet) for yeet in songframes]))

print(len(songframes))
 
def note_to_freq(note='C-4'):
    #from https://www.devrs.com/gb/files/sndtab.html
    _oct=3
    if note==f'C-{_oct}': return 44
    if note==f'C#{_oct}': return 156
    if note==f'D-{_oct}': return 262
    if note==f'D#{_oct}': return 363
    if note==f'E-{_oct}': return 457
    if note==f'F-{_oct}': return 547
    if note==f'F#{_oct}': return 631
    if note==f'G-{_oct}': return 710
    if note==f'G#{_oct}': return 786
    if note==f'A-{_oct}': return 854
    if note==f'A#{_oct}': return 923
    if note==f'B-{_oct}': return 986
    _oct=4
    if note==f'C-{_oct}': return 1046
    if note==f'C#{_oct}': return 1102
    if note==f'D-{_oct}': return 1155
    if note==f'D#{_oct}': return 1205
    if note==f'E-{_oct}': return 1253
    if note==f'F-{_oct}': return 1297
    if note==f'F#{_oct}': return 1339
    if note==f'G-{_oct}': return 1379
    if note==f'G#{_oct}': return 1417
    if note==f'A-{_oct}': return 1452
    if note==f'A#{_oct}': return 1486
    if note==f'B-{_oct}': return 1517
    _oct=5
    if note==f'C-{_oct}': return 1546
    if note==f'C#{_oct}': return 1575
    if note==f'D-{_oct}': return 1602
    if note==f'D#{_oct}': return 1627
    if note==f'E-{_oct}': return 1650
    if note==f'F-{_oct}': return 1673
    if note==f'F#{_oct}': return 1694
    if note==f'G-{_oct}': return 1714
    if note==f'G#{_oct}': return 1732
    if note==f'A-{_oct}': return 1750
    if note==f'A#{_oct}': return 1767
    if note==f'B-{_oct}': return 1783
    _oct=6
    if note==f'C-{_oct}': return 1798
    if note==f'C#{_oct}': return 1812
    if note==f'D-{_oct}': return 1825
    if note==f'D#{_oct}': return 1837
    if note==f'E-{_oct}': return 1849
    if note==f'F-{_oct}': return 1860
    if note==f'F#{_oct}': return 1871
    if note==f'G-{_oct}': return 1881
    if note==f'G#{_oct}': return 1890
    if note==f'A-{_oct}': return 1899
    if note==f'A#{_oct}': return 1907
    if note==f'B-{_oct}': return 1915
    _oct=7
    if note==f'C-{_oct}': return 1923
    if note==f'C#{_oct}': return 1930
    if note==f'D-{_oct}': return 1936
    if note==f'D#{_oct}': return 1943
    if note==f'E-{_oct}': return 1949
    if note==f'F-{_oct}': return 1954
    if note==f'F#{_oct}': return 1959
    if note==f'G-{_oct}': return 1964
    if note==f'G#{_oct}': return 1969
    if note==f'A-{_oct}': return 1974
    if note==f'A#{_oct}': return 1978
    if note==f'B-{_oct}': return 1982
    _oct=8
    if note==f'C-{_oct}': return 1985
    if note==f'C#{_oct}': return 1988
    if note==f'D-{_oct}': return 1992
    if note==f'D#{_oct}': return 1995
    if note==f'E-{_oct}': return 1998
    if note==f'F-{_oct}': return 2001
    if note==f'F#{_oct}': return 2004
    if note==f'G-{_oct}': return 2006
    if note==f'G#{_oct}': return 2009
    if note==f'A-{_oct}': return 2011
    if note==f'A#{_oct}': return 2013
    if note==f'B-{_oct}': return 2015
    


quiet = False

romfile='game.gb'

global reg_updates
reg_updates=0
def mem(adr,val):
    pyboy.set_memory_value(int(adr,base=16),val)
    
def mem_int(adr,val):
    pyboy.set_memory_value(adr,val)

def binary(val):
    return int(val,base=2)

#load a dummy game in - this is from https://github.com/assemblydigest/gameboy/tree/master/part-1-make-a-gb-rom/rgbds
pyboy = PyBoy(romfile, sound=True, window_type="headless" if quiet else "SDL2", window_scale=3, debug=debug, game_wrapper=True)


frame_=0
pyboy.set_emulation_speed(0) #uncap emulation speed so that it can run AFAP
with open('tilemap_stream.bin','rb') as f:
    tilemap_stream=f.read()
with open('tileset_stream.bin','rb') as f:
    tileset_stream=f.read()

def trigger_ch2(pitch=1024,volume=15,direction=0,pace=1,duty=0,length=False):    
    _pch=bin(pitch % 2048)[2:].zfill(11)
    _vol=bin(volume % 16)[2:].zfill(4)
    _pce=bin(pace % 8)[2:].zfill(3)
    _dir=str(direction % 2)
    _dty=bin(duty % 4)[2:].zfill(2)
    #print(_dty)
    _lgh=bin(length % 64)[2:].zfill(6) if length!=False else '0'
    _lghenable='1' if length!=False else '0'
    _pch1=_pch[:3]
    _pch2=_pch[3:]

    #for some reason duty is suddenly not working despite everything pointing to it
    #should working AND it working before
    
    mem('FF16',binary(_dty+_lgh)) #length duty
    mem('FF17',binary(_vol+_dir+_pce)) #volume envelope
    mem('FF18',binary(_pch2)) #pitch 1
    mem('FF19',binary('1'+_lghenable+'000'+_pch1)) #pitch 2
beat=0
pitch=0
vgm_i=0
song_i=0
cycle=0
startTime = time.time()
cmd='balls'
lastcmd='balls2'
refresh_rate=60

while True:
    start = time.time()
    frame=round(frame_)

    #turn on sound
    #mem('FF26',binary('10001111')) #the 1111 are read only but im writing em anyways
    pitch=pitch%2048
    lastcmd=cmd
    
    if cycle>40:
        for songrow in songframes[song_i]:
            #print(songrow)
                
            cmd=songrow[12:14]
            reg=songrow[15:17]
            val=songrow[18:20]

            if reg=='06': #CH 2 Duty, Length
                mem('FF16',int(val,base=16))
            if reg=='07': #CH 2 Envelope
                mem('FF17',int(val,base=16))
            if reg=='08': #CH 2 Frequency LSB
                mem('FF18',int(val,base=16))
            if reg=='09': #CH 2 Trigger, Frequency MSB, Mode
                mem('FF19',int(val,base=16))

            if reg=='00': #CH 1 Sweep
                mem('FF10',int(val,base=16))
            if reg=='01': #CH 1 Duty, Length
                mem('FF11',int(val,base=16))
            if reg=='02': #CH 1 Envelope
                mem('FF12',int(val,base=16))
            if reg=='03': #CH 1 Frequency LSB
                mem('FF13',int(val,base=16))
            if reg=='04': #CH 1 Trigger, Frequency MSB, Mode
                mem('FF14',int(val,base=16))

            if reg=='0A': #CH 3 DAC Off/On
                mem('FF1A',int(val,base=16))
            if reg=='0B': #CH 3 Length Timer?
                mem('FF1B',int(val,base=16))
            if reg=='0C': #CH 3 Level
                mem('FF1C',int(val,base=16))
            if reg=='0D': #CH 3 Frequency LSB
                mem('FF1D',int(val,base=16))
            if reg=='0E': #CH 3 Trigger, Frequency MSB, Mode
                mem('FF1E',int(val,base=16))

            #wave pattern RAM
            for reg_i in range(16):
                vgm_reg_base=int('20',base=16)
                dmg_reg_base=int('FF30',base=16)
                
                vgm_reg_int=vgm_reg_base+reg_i
                dmg_reg_int=dmg_reg_base+reg_i

                vgm_reg=hex(vgm_reg_int)[2:].upper()
                dmg_reg=hex(dmg_reg_int)[2:].upper()
                if reg==vgm_reg:
                    mem(dmg_reg,int(val,base=16))
                    break

            if reg=='10': #CH N Length
                mem('FF20',int(val,base=16))
            if reg=='11': #CH N Envelope
                mem('FF21',int(val,base=16))
            if reg=='12': #CH N Freq
                mem('FF22',int(val,base=16))
            if reg=='13': #CH N Mode
                mem('FF23',int(val,base=16))

            if reg=='14': #Master Volume
                mem('FF24',int(val,base=16))
            if reg=='15': #Panning
                mem('FF25',int(val,base=16))
            if reg=='16': #Sound Off/On
                mem('FF26',int(val,base=16))
        song_i+=1
    
    #end vgm playback code
    
    pitch+=10
    
    #override scroll
    mem('FF42',0)
    mem('FF43',0)
    #override lcd settings
    mem('FF40',int('10010001',base=2))
    #override monochrome palette
    mem('FF47',int('00011011',base=2))
    i2=0

    tileset_offset=frame*3072
    tilemap_offset=frame*1024
    #copy tilesets to vram
    for i in range(tileset_offset,tileset_offset+3072):
        mem_int(int('8000',base=16)+i2,tileset_stream[i])
        i2+=1
    i2=0
    #copy tilemaps to vram
    for i in range(tilemap_offset,tilemap_offset+576): #only copy first 576 y's
        if i2%32<20: #only copy first 20 x's
            mem_int(int('9800',base=16)+i2,tilemap_stream[i])
        i2+=1
    #i2
    end = time.time()-start
    
    pyboy.tick()
    #better timing since .tick() is blocking - still not perfect though
    while end<(1/refresh_rate):
        end = time.time()-start
        pass
    #print(reg_updates)
    reg_updates=0
    frame_+=0.4 #play at 24fps
    cycle+=1





