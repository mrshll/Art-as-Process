#!/usr/bin/env python
import alsaaudio, sys
import time

channels = 1
sample_size = 1
frame_size = channels * sample_size
frame_rate = 44100
byte_rate = frame_rate * frame_size

#******************************************************************
#******************************************************************
#               OUTPUT                                       *
#period size controls internal number of frames per period
period_size = 160

out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, card='default')

out.setchannels(channels)
out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
out.setrate(frame_rate)
out.setperiodsize(period_size)

#******************************************************************
#******************************************************************
#                       INPUT                                   *

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, 'default')

inp.setchannels(channels)
inp.setrate(frame_rate)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)#16 bit little endian
inp.setperiodsize(period_size)

#******************************************************************

def main():
   buf = []
   #count = 0
   while True:
       l, data = inp.read()
       buf.append(data)
       if len(buf)>=50000:
           out.write(buf[0])
           #if count % 100 == 0:
               #print(buf[0])
           #count +=1
           del buf[0]

if __name__ == '__main__':
    main()
