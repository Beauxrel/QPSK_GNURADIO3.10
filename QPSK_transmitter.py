#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK Transmitter with differential coding
# Author: Manolis Bozis
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import QPSK_transmitter_epy_module_0 as epy_module_0  # embedded python module
import QPSK_transmitter_epy_module_1 as epy_module_1  # embedded python module
import math
import numpy
import sip



class QPSK_transmitter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK Transmitter with differential coding", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QPSK Transmitter with differential coding")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "QPSK_transmitter")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.Taps_No = Taps_No = 31
        self.Mod_Ind = Mod_Ind = 4
        self.sps = sps = 4
        self.Symbol_Map = Symbol_Map = epy_module_1.gray2int( int( math.log(Mod_Ind, 2.0) ) )
        self.Rs = Rs = 480000
        self.Delay = Delay = int((Taps_No-1)/2)
        self.Const_Pnts = Const_Pnts = epy_module_0.PSKsymbols(Mod_Ind)
        self.var_const = var_const = digital.constellation_calcdist(Const_Pnts, Symbol_Map,
        Mod_Ind, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.transition = transition = 100
        self.timing_offset = timing_offset = 1.0
        self.squelch = squelch = -10
        self.samp_rate = samp_rate = Rs*sps
        self.preample_length = preample_length = 2*8
        self.noise = noise = 0.0
        self.message_length = message_length = 44153*8
        self.message_bytes = message_bytes = 44153
        self.frequency_offset = frequency_offset = 0.0
        self.cutoff = cutoff = 1000
        self.alpha = alpha = 0.35
        self.RC_Delay = RC_Delay = sps-(2*Delay+1)%sps
        self.QPSK = QPSK = digital.constellation_calcdist(Const_Pnts, Symbol_Map,
        Mod_Ind, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.Points = Points = 10
        self.Carrier_Frequency = Carrier_Frequency = 735e6

        ##################################################
        # Blocks
        ##################################################

        self._timing_offset_range = Range(1.0, 1.001, 1e-6, 1.0, 200)
        self._timing_offset_win = RangeWidget(self._timing_offset_range, self.set_timing_offset, "timing offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._timing_offset_win)
        self._squelch_range = Range(-200, -10, 5, -10, 200)
        self._squelch_win = RangeWidget(self._squelch_range, self.set_squelch, "squelch", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._squelch_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(0.0, 0.2, 0.005, 0.0, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, "Noise Voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_win)
        self._frequency_offset_range = Range(0.0, 1e-5, 10e-9, 0.0, 200)
        self._frequency_offset_win = RangeWidget(self._frequency_offset_range, self.set_frequency_offset, "frequency_offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._frequency_offset_win)
        self._transition_range = Range(0.0, 10000, 100, 100, 200)
        self._transition_win = RangeWidget(self._transition_range, self.set_transition, "transition", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._transition_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_ccf(
            sps,
            firdes.root_raised_cosine(
                1,
                (Rs*sps),
                Rs,
                alpha,
                Taps_No))
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            (sps*Points), #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            Points, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (float(samp_rate*sps)), #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            2048, #size
            'Rx Constellation Diagram Sync', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "QPSK Constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('ip:192.168.50.236' if 'ip:192.168.50.236' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('')
        self.iio_pluto_source_0.set_frequency(2400000000)
        self.iio_pluto_source_0.set_samplerate(int(samp_rate))
        self.iio_pluto_source_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0.set_gain(0, 70)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('ip:192.168.50.236' if 'ip:192.168.50.236' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0.set_frequency(2400000000)
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, 5.0)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, .0628, firdes.root_raised_cosine(32, 32*sps, 1.0,alpha,sps*11*32), 32, 16, 1.5, 1)
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(Mod_Ind, digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(Mod_Ind, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_1 = digital.costas_loop_cc((2*math.pi/100), Mod_Ind, False)
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_bb('11100001010110101110100010010011', 0, '')
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(QPSK)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(Const_Pnts, 1)
        self._cutoff_range = Range(0.0, 100000, 1000, 1000, 200)
        self._cutoff_win = RangeWidget(self._cutoff_range, self.set_cutoff, "cutoff", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._cutoff_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise,
            frequency_offset=frequency_offset,
            epsilon=timing_offset,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((1,1,1,0,0,0,0,1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,1,0,0,1,1), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_char*1, 'burst')
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_streams_0 = blocks.stream_to_streams(gr.sizeof_char*1, 2)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (16, 488))
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(2, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(2, 1, "", False, gr.GR_LSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(int(math.log(Mod_Ind, 2)), gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(1)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_char, message_length, (message_length+preample_length), 0)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, 'C:\\Users\\Landon\\Desktop\\Landon\\QPSK\\tx\\text_send.txt', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_0_1 = blocks.file_sink(gr.sizeof_char*1, 'C:\\Users\\Landon\\Desktop\\Landon\\QPSK\\rx\\TXTout.txt', False)
        self.blocks_file_sink_0_0_1.set_unbuffered(False)
        self.blocks_char_to_short_0 = blocks.char_to_short(1)
        self.blocks_burst_tagger_0 = blocks.burst_tagger(gr.sizeof_char)
        self.blocks_burst_tagger_0.set_true_tag('burst',True)
        self.blocks_burst_tagger_0.set_false_tag('burst',False)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(squelch, 1)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(sps, 2)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.blocks_burst_tagger_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.blocks_char_to_short_0, 0), (self.blocks_burst_tagger_0, 1))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_unpacked_to_packed_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_stream_to_streams_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_stream_to_streams_0, 0), (self.blocks_burst_tagger_0, 0))
        self.connect((self.blocks_stream_to_streams_0, 1), (self.blocks_char_to_short_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0_0, 0), (self.blocks_file_sink_0_0_1, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_1, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_time_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "QPSK_transmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_Taps_No(self):
        return self.Taps_No

    def set_Taps_No(self, Taps_No):
        self.Taps_No = Taps_No
        self.set_Delay(int((self.Taps_No-1)/2))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.Rs*self.sps), self.Rs, self.alpha, self.Taps_No))

    def get_Mod_Ind(self):
        return self.Mod_Ind

    def set_Mod_Ind(self, Mod_Ind):
        self.Mod_Ind = Mod_Ind
        self.set_Const_Pnts(epy_module_0.PSKsymbols(self.Mod_Ind))
        self.set_Symbol_Map(epy_module_1.gray2int( int( math.log(self.Mod_Ind, 2.0) ) ))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_RC_Delay(self.sps-(2*self.Delay+1)%self.sps)
        self.set_samp_rate(self.Rs*self.sps)
        self.digital_pfb_clock_sync_xxx_0.update_taps(firdes.root_raised_cosine(32, 32*self.sps, 1.0,self.alpha,self.sps*11*32))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, (float(self.samp_rate*self.sps)))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.Rs*self.sps), self.Rs, self.alpha, self.Taps_No))

    def get_Symbol_Map(self):
        return self.Symbol_Map

    def set_Symbol_Map(self, Symbol_Map):
        self.Symbol_Map = Symbol_Map

    def get_Rs(self):
        return self.Rs

    def set_Rs(self, Rs):
        self.Rs = Rs
        self.set_samp_rate(self.Rs*self.sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.Rs*self.sps), self.Rs, self.alpha, self.Taps_No))

    def get_Delay(self):
        return self.Delay

    def set_Delay(self, Delay):
        self.Delay = Delay
        self.set_RC_Delay(self.sps-(2*self.Delay+1)%self.sps)

    def get_Const_Pnts(self):
        return self.Const_Pnts

    def set_Const_Pnts(self, Const_Pnts):
        self.Const_Pnts = Const_Pnts
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.Const_Pnts)

    def get_var_const(self):
        return self.var_const

    def set_var_const(self, var_const):
        self.var_const = var_const

    def get_transition(self):
        return self.transition

    def set_transition(self, transition):
        self.transition = transition

    def get_timing_offset(self):
        return self.timing_offset

    def set_timing_offset(self, timing_offset):
        self.timing_offset = timing_offset
        self.channels_channel_model_0.set_timing_offset(self.timing_offset)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.analog_simple_squelch_cc_0.set_threshold(self.squelch)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.iio_pluto_source_0.set_samplerate(int(self.samp_rate))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, (float(self.samp_rate*self.sps)))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_preample_length(self):
        return self.preample_length

    def set_preample_length(self, preample_length):
        self.preample_length = preample_length
        self.blocks_keep_m_in_n_0.set_n((self.message_length+self.preample_length))

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0.set_noise_voltage(self.noise)

    def get_message_length(self):
        return self.message_length

    def set_message_length(self, message_length):
        self.message_length = message_length
        self.blocks_keep_m_in_n_0.set_m(self.message_length)
        self.blocks_keep_m_in_n_0.set_n((self.message_length+self.preample_length))

    def get_message_bytes(self):
        return self.message_bytes

    def set_message_bytes(self, message_bytes):
        self.message_bytes = message_bytes

    def get_frequency_offset(self):
        return self.frequency_offset

    def set_frequency_offset(self, frequency_offset):
        self.frequency_offset = frequency_offset
        self.channels_channel_model_0.set_frequency_offset(self.frequency_offset)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.digital_pfb_clock_sync_xxx_0.update_taps(firdes.root_raised_cosine(32, 32*self.sps, 1.0,self.alpha,self.sps*11*32))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.Rs*self.sps), self.Rs, self.alpha, self.Taps_No))

    def get_RC_Delay(self):
        return self.RC_Delay

    def set_RC_Delay(self, RC_Delay):
        self.RC_Delay = RC_Delay

    def get_QPSK(self):
        return self.QPSK

    def set_QPSK(self, QPSK):
        self.QPSK = QPSK
        self.digital_constellation_decoder_cb_0.set_constellation(self.QPSK)

    def get_Points(self):
        return self.Points

    def set_Points(self, Points):
        self.Points = Points

    def get_Carrier_Frequency(self):
        return self.Carrier_Frequency

    def set_Carrier_Frequency(self, Carrier_Frequency):
        self.Carrier_Frequency = Carrier_Frequency




def main(top_block_cls=QPSK_transmitter, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
