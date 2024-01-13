from pyboy import PyBoy
import time
debug=False


quiet = False
#load a dummy game in - this is from https://github.com/assemblydigest/gameboy/tree/master/part-1-make-a-gb-rom/rgbds
pyboy = PyBoy('game.gb', window_type="headless" if quiet else "SDL2", window_scale=3, debug=debug, game_wrapper=True)


frame_=0
pyboy.set_emulation_speed(0) #uncap emulation speed so that it can run AFAP
with open('tilemap_stream.bin','rb') as f:
    tilemap_stream=f.read()
with open('tileset_stream.bin','rb') as f:
    tileset_stream=f.read()
    
while True:
    start = time.time()
    frame=round(frame_)

    #override scroll
    pyboy.set_memory_value(int('FF42',base=16),0)
    pyboy.set_memory_value(int('FF43',base=16),0)
    #override lcd settings
    pyboy.set_memory_value(int('FF40',base=16),int('10010001',base=2))
    #override monochrome palette
    pyboy.set_memory_value(int('FF47',base=16),int('00011011',base=2))
    i2=0

    tileset_offset=frame*3072
    tilemap_offset=frame*1024
    #copy tilesets to vram
    for i in range(tileset_offset,tileset_offset+3072):
        pyboy.set_memory_value(int('8000',base=16)+i2,tileset_stream[i])
        i2+=1
    i2=0
    #copy tilemaps to vram
    for i in range(tilemap_offset,tilemap_offset+576): #only copy first 576 y's
        if i2%32<20: #only copy first 20 x's
            pyboy.set_memory_value(int('9800',base=16)+i2,tilemap_stream[i])
        i2+=1
    #i2
    end = time.time()-start
    
    pyboy.tick()
    #better timing since .tick() is blocking - still not perfect though
    while end<(1/60):
        end = time.time()-start
        pass 
    frame_+=0.4 #play at 24fps





