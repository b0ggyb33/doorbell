#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Fri Feb 13 17:11:51 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx
import time
from pushbullet import Pushbullet

class top_block(gr.top_block):#grc_wxgui.top_block_gui):
    def recv_pkt(self):
        pkt = 0

        if self.sink_queue.count():
            pkt = self.sink_queue.delete_head().to_string()
        
        return pkt
    
    def packet_as_ints(self):
        myInts = [x for x in bytearray(self.recv_pkt())]
        return myInts
    
    def packetsAboveZero(self):
        ints=self.packet_as_ints()
        return sum(ints)
        
    def __init__(self):
        gr.top_block.__init__(self)
        #_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        #self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 96e3
        self.frequency = frequency = 433.967e6
	self.threshold = 0.06

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(1, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.sink_queue = gr.msg_queue()  
          
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0, self.threshold, 0)
        self.blocks_message_sink_0 = blocks.message_sink(gr.sizeof_char*1, self.sink_queue, True)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_real_0, 0))
        #self.connect((self.blocks_message_sink_0, msg), (self, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_message_sink_0, 0))
        #self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_message_sink_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.rtlsdr_source_0.set_center_freq(self.frequency, 0)


def dingdong():
    print "dingDong"
    pb.push_note("Door Bell","Ding Dong!")
    

if __name__ == '__main__':
    import ctypes
    import os
    api_key='IQCoV2PuDYmXSiKbUxv9dIFQYwVeKBUQ'
    pb = Pushbullet(api_key)
    
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    #tb.Start(True)
    tb.run()
    
    lastTime=0
    
    while True:
        nonZeroPackets=tb.packetsAboveZero() 
	#print nonZeroPackets
        if nonZeroPackets> 0:
            timeNow=time.time()
            if (timeNow - lastTime) > 5:
                dingdong()
                lastTime=timeNow
            
        #sleep(0.1)

