import os
import PIL
from PIL import Image,ImageOps
import math
import numpy as np
import json

videoFile=r'kemono_friends_ncop_ep10.mkv'

#make directory for frames - should make this os.mkdir but would
#require writing if elses for all the other mkdirs because they
#like to nag when the directory exists cause theyre lame
os.system('mkdir videoFrames')

#convert input video to 160x144 pngs
os.system('ffmpeg -i "'+videoFile+'" -vf scale=160x144 videoFrames/%04d.png -y')


os.system('mkdir convertedFrames')



#preprocess

g=len(os.listdir('videoFrames'))
for frame,i in enumerate(os.listdir('videoFrames')):
    #print(i)
    InFrame=Image.open('videoFrames/'+i)
    InFrame=InFrame.convert('L')#make it bw
    InFrame=ImageOps.autocontrast(InFrame, cutoff=0) #contrast
    pixels = InFrame.load()

    for x in range(InFrame.size[0]):
        for y in range(InFrame.size[1]):
            #quantize all the values to 4 colors
            p=pixels[x,y]
            if p >= 0 and p <= 63:
                pixels[x,y] = 0
            if p >= 64 and p <= 127:
                pixels[x,y] = 85
            if p >= 128 and p <= 191:
                pixels[x,y] = 170
            if p >= 192 and p <= 255:
                pixels[x,y] = 255
    InFrame.save('convertedFrames/'+i) #save converted frame

    #PROGRESSBAR CODE i shoulda made this a funky wunction
    prgb_len=50
    prgb=''
    prc=frame/g
    for i2 in range(round(prgb_len*prc)):
        prgb+='O'
    for i2 in range(prgb_len-len(prgb)):
        prgb+='-'
    prc_true=str(round(prc*100)).rjust(3)
    print(f'{prc_true}% | {prgb} | {frame}/{g}')

#generate gameboy imgs!

os.system('mkdir previewFrames')

#generate spiral
#this spiral is to optimize tile generation so that the parts
#closest to the center are prioritized
spiralTable=[]
basex=5000
basey=5000
print('generating spiral')
for radius_ in range(0,100):
    radius=radius_*100
    for deg in range(0,360):
        rad=math.radians(deg)
        x=basex+(math.sin(rad)*radius)
        y=basey+(math.cos(rad)*radius)
        true_x=max(0,min(round((x/10000)*20),19))
        true_y=max(0,min(round((y/10000)*18),17))
        coord=[true_x,true_y]
        if coord not in spiralTable: spiralTable.append(coord)
    #if radius%100==0: print(radius)
        
#debugging spiral location and size - i originally had it divide by 5k instead of 10k and it caused a quadricircle instead of a circle
##debugSpiral=Image.new('RGB',(20,18),(255,255,255))
##pixels=debugSpiral.load()
##for i2,i in enumerate(spiralTable):
##    pixels[i[0],i[1]]=(i2%256,i2//256,0)
##
##debugSpiral.save('debugSpiral.png')
#print(BreakCodeHerePlz) #rudimentary breakpoint

#debug code for detecting unfilled blocks, was used during
#when i was optimizing the spiral radius to not take forever while still
#covering all 20x18 tiles
##unfilled=[]
##for y in range(18):
##    for x in range(20):
##        if [x,y] not in spiralTable: unfilled.append([x,y])
##print(f'UNFILLED BLOCKS: {unfilled}')

#these are the txt files describing tilemaps/sets
        #why am i doing txt instead of directly writing them? idk
        # but partly because i was doing this program in chunks
        #but still able to be run as one script
        #idk how to word this
os.system('mkdir unprocessed_tilemaps')
os.system('mkdir unprocessed_tilesets')

g=len(os.listdir('convertedFrames'))
for frame,i in enumerate(os.listdir('convertedFrames')):
    InFrame=Image.open('convertedFrames/'+i)
    tiles=[]
    #max of 192 tiles

    #ok so it will go like this:
    #generate tile for every 8x8 tile in frame
    #remove redundant ones
    #assign all matching ones
    #for the remainder (if they didnt fit) use some hamming type beat shtuff
    #or something to find the closest matching tile

    #i ended up using euclidean distance

    #pogress bartholomew
    prgb_len=50
    prgb=''
    prc=frame/g
    for i2 in range(round(prgb_len*prc)):
        prgb+='O'
    for i2 in range(prgb_len-len(prgb)):
        prgb+='-'
    prc_true=str(round(prc*100)).rjust(3)
    print(f'{prc_true}% | {prgb} | {frame}/{g}')

    
    pixels=InFrame.load()
    #code was scrapped because i used the spiral method
    #instead of going top to bottom left to right
##    for tile_y in range(18):
##        for tile_x in range(20):
##            tile=[]
##            for pixel_y in range(8):
##                for pixel_x in range(8):
##                    val=pixels[(tile_x*8)+pixel_x,(tile_y*8)+pixel_y]
##                    if val==0: val=0
##                    if val==85: val=1
##                    if val==170: val=2
##                    if val==255: val=3
##                    tile.append(val)
##            tiles.append(tile)
    
    #spiral center ver
    for coords in spiralTable:
        tile_x=coords[0]
        tile_y=coords[1]
        tile=[]
        for pixel_y in range(8):
            for pixel_x in range(8):
                val=pixels[(tile_x*8)+pixel_x,(tile_y*8)+pixel_y]
                if val==0: val=0
                if val==85: val=1
                if val==170: val=2
                if val==255: val=3
                tile.append(val)
        tiles.append(tile)
    
    tiles_reduced=[]
    #remove duplicate tiles
    for tile in tiles:
        if tile not in tiles_reduced: tiles_reduced.append(tile)

    #coders note: if i was on GBC id be able to a. fit all 360 tiles in
        #vram and b. flip tiles horizontally and vertically

        #but thats not fun!! dmg funny
        
    print(f'tiles before reduction: {len(tiles)}')
    print(f'tiles after basic reduction: {len(tiles_reduced)}')
    tiles_reduced=tiles_reduced[:192] #truncate to 192 tiles
    tilei=0
    #make tilemap
    previewImage=Image.new('L',(160,144),color=255)
    tilemap=[0]*360
    for tile_y in range(18):
        for tile_x in range(20):
            tile=[]
            for pixel_y in range(8):
                for pixel_x in range(8):
                    val=pixels[(tile_x*8)+pixel_x,(tile_y*8)+pixel_y]
                    if val==0: val=0
                    if val==85: val=1
                    if val==170: val=2
                    if val==255: val=3
                    tile.append(val)
            #do comparison shtuff
            
            val=-1
            #substitute any matches with matches
            for tileIDX,realTile in enumerate(tiles_reduced):
                if realTile==tile:
                    val=tileIDX
            if val==-1:
                #fallback: calculate distance
                lowestDistance=10000000 #rughgh
                tileWithLowestDistance=0
                for tileIDX,realTile in enumerate(tiles_reduced):
                    np_realTile=np.array(realTile)
                    np_tile=np.array(tile)
                    distance=np.sum((np_tile-np_realTile)**2)
                    if distance<lowestDistance:
                        lowestDistance=distance
                        tileWithLowestDistance=tileIDX
                val=tileWithLowestDistance

                    
            tilemap[tilei]=val
            
            
                
            tilei+=1
    #i was stupid
    with open('unprocessed_tilemaps/'+i.split('.')[0]+'.txt','w') as f:
        f.write('\n'.join([str(this) for this in tilemap]))

    with open('unprocessed_tilesets/'+i.split('.')[0]+'.txt','w') as f:
        f.write('\n'.join([str(this) for this in tiles_reduced]))
            
    #preview shtuff please remove for faster code because this
    #is a bottleneck
    pixels=previewImage.load()
    for tilei,tile_ref in enumerate(tilemap):
        tile=tiles_reduced[tile_ref]
        x2=tilei %  20
        y2=tilei // 20
        for y in range(8):
            for x in range(8):
                val=tile[(y*8)+x]*63
                pixels[(x2*8)+x,(y2*8)+y]=val
    previewImage.save('previewFrames/'+i)
                
    #awful variable names. this was debug for the arrays
##    jeep=''
##    jeep2=''
##    jeepcounter=0
##    for yai in tilemap:
##        jeep+=str(yai).rjust(3)+', '
##        jeepcounter+=1
##        if jeepcounter==20:
##            jeepcounter=0
##            jeep2+=jeep+'\n'
##            jeep=''
##    print(jeep2)
        

#now, convert those dang-donkey txt files into binary code
tileset_stream=[]
tilemap_stream=[]
for frame,i in enumerate(os.listdir('unprocessed_tilesets')):
    #print(i)
    with open('unprocessed_tilesets/'+i,'r') as f:
        ts=f.read().split('\n')
    with open('unprocessed_tilemaps/'+i,'r') as f:
        tm=f.read().split('\n')
    tileset=[0]*(3072)
    tilemap=[0]*1024
    
    tileset_temp=[]
    tilemap_temp=[]
    for tile_ in ts:
        tile=json.loads(tile_)
        #print(tile)
        for y in range(8):
            row=[0]*16
            for x in range(8):
                #OH GOD WHAT IS THIS

                #ok so this: ill go into detail
                #the gameboy graphics are two planes per row
                #two 1bpp planes that make up a 2bpp row
                #so assume: the first pixel is either 0 1 2 3 it will be:
                #0: 00000000 00000000
                #1: 10000000 00000000
                #2: 00000000 10000000
                #3: 10000000 10000000

                #ignore the parenthesized X
                if tile[(y*8)+x]==0:
                    row[(x)+0]=0
                    row[(x)+8]=0
                if tile[(y*8)+x]==1:
                    row[(x)+0]=1
                    row[(x)+8]=0
                if tile[(y*8)+x]==2:
                    row[(x)+0]=0
                    row[(x)+8]=1
                if tile[(y*8)+x]==3:
                    row[(x)+0]=1
                    row[(x)+8]=1
            row_true=''.join([str(px) for px in row])
            #print(row_true)
            #split the bitplanes
            row=int(row_true[:8],base=2)
            tileset_temp.append(row)
            row=int(row_true[8:],base=2)
            tileset_temp.append(row)
            
    #transfer temporary truncated tileset into the fullsize tileset
    for ti,tt in enumerate(tileset_temp):
        tileset[ti]=tt
    #now add that 192-tile tileset to the stream
    for i in tileset:
        tileset_stream.append(i)
    i2=0
    #now make a temporary tilemap
    for y in range(18):
        for x in range(20):
            tilemap_temp.append(int(tm[i2]))
            i2+=1
        for x in range(32-20):
            tilemap_temp.append(0)
    
    #blah blah
    for ti,tt in enumerate(tilemap_temp):
        tilemap[ti]=tt
        
    #move that to the stream
    for i in tilemap:
        tilemap_stream.append(i)

    #print('-----')
    #Pregnant barf
    prgb_len=50
    prgb=''
    prc=frame/g
    for i2 in range(round(prgb_len*prc)):
        prgb+='O'
    for i2 in range(prgb_len-len(prgb)):
        prgb+='-'
    prc_true=str(round(prc*100)).rjust(3)
    print(f'{prc_true}% | {prgb} | {frame}/{g}')
    #with open('tilemap_stream.bin','wb') as f:
        #f.write(bytes(tilemap_stream))

#FINALLY write that shtuff to a bin file that can be
#directly pumped into the gameboy vram via some
#frankenstein script
with open('tileset_stream.bin','wb') as f:
        f.write(bytes(tileset_stream))
with open('tilemap_stream.bin','wb') as f:
        f.write(bytes(tilemap_stream))
    










