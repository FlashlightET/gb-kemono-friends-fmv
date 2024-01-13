game boy frame boy


<p>
  <center>
    <img src="https://github.com/FlashlightET/gb-kemono-friends-fmv/assets/29938499/37843881-2a4c-4066-a033-ccc7fea9fccd" width="300" />
    <img src="https://github.com/FlashlightET/gb-kemono-friends-fmv/assets/29938499/8d006a00-d5e2-4fa5-9b90-d7c9a46b78b4" width="300" /> 
    <img src="https://github.com/FlashlightET/gb-kemono-friends-fmv/assets/29938499/9e3b2832-422f-48c4-921d-350deec09eda" width="300" />
  </center>
</p>
thing i pumped out lol

i dont think the DMG gameboy has enough power to do this on its own even with bankswitching

but the stuff you can do with modern software

requires pyboy and coded in python 3.7 but new python should work, however it was coded on windows so if anything breaks its probably a linux thing idk or mac if youre a weirdo

also requires numpy for literally one line of code (three actually)

no audio support yet (id make a whole sequence format just for that lol, im the type to do that)

# playback

running `playback.py` will playback `tileset_stream.bin` and `tilemap_stream.bin` into an emulated gameboy's vram.

requires dummy gameboy rom to run, i used the one from here https://github.com/assemblydigest/gameboy/tree/master/part-1-make-a-gb-rom/rgbds

the pyboy bootscreen will cause a wavy distortion in the first second or so

# stream generation

`convertVideo.py` converts a video to two streams: `tileset_stream.bin` and `tilemap_stream.bin`. their contents and purposes should be self-explanatory.

stream generation requires a legally obtained copy of `kemono_friends_ncop_ep10.mkv` (not supplied) (doesnt have to be `kemono_friends_ncop_ep10.mkv`)

also ffmpeg (note: not *ffmpreg*! do not make the mistake i made)

