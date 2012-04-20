#!/usr/bin/env python

# This is some example code for python-gstreamer.
# It's a gstreamer TCP/IP client that sends a file
# through a tcpclientsink to a server on localhost

import gobject, pygst
pygst.require("0.10")
import gst
import sys

try:
        DELAY = float(sys.argv[1])
        DELAY = long(DELAY * 1000000000)
        print DELAY
except IndexError:
        DELAY = 0

# create a pipeline and add [ filesrc ! tcpclientsink ]
pipeline = gst.Pipeline("client")

#ALSA
audiosrc = gst.element_factory_make("alsasrc", "audio")
audiosrc.set_property("device","default")
pipeline.add(audiosrc)

#Queue
audioqueue = gst.element_factory_make("queue","queue1")
audioqueue.set_property("max-size-time",0)
audioqueue.set_property("max-size-buffers",0)
audioqueue.set_property("max-size-bytes",0)
audioqueue.set_property("min-threshold-time",DELAY)
audioqueue.set_property("leaky","no")
pipeline.add(audioqueue)


#Link the elements
client = gst.element_factory_make("tcpclientsink", "client")
pipeline.add(client)
client.set_property("host", "127.0.0.1")
client.set_property("port", 3000)
audioqueue.link(client)

#Begin Playing
pipeline.set_state(gst.STATE_PLAYING)

# enter into a mainloop
loop = gobject.MainLoop()
loop.run()

