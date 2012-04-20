#!/usr/bin/env python

# This is some example code for python-gstreamer.
# It's a gstreamer TCP/IP client that sends a file
# through a tcpclientsink to a server on localhost

import gobject, pygst
pygst.require("0.10")
import gst
import sys

DELAY = long(10 * 1000000000)

# create a pipeline and add [ filesrc ! tcpclientsink ]
pipeline = gst.Pipeline("client")

#ALSA
src = gst.element_factory_make("alsasrc", "audio")
src.set_property("device","default")
pipeline.add(src)

#Queue
audioqueue = gst.element_factory_make("queue","queue1")
audioqueue.set_property("max-size-time",0)
audioqueue.set_property("max-size-buffers",0)
audioqueue.set_property("max-size-bytes",0)
audioqueue.set_property("min-threshold-time",DELAY)
audioqueue.set_property("leaky","no")
pipeline.add(audioqueue)

#CONVERT
convert = gst.element_factory_make("audioconvert", "convert")
pipeline.add(convert)

#FLACENC
flacenc = gst.element_factory_make("flacenc", "encoder")
pipeline.add(flacenc)

#Link the elements
client = gst.element_factory_make("tcpclientsink", "client")
pipeline.add(client)
client.set_property("host", "127.0.0.1")
client.set_property("port", 3000)
gst.element_link_many(src, audioqueue, convert, flacenc, client)

#Begin Playing
pipeline.set_state(gst.STATE_PLAYING)

# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

