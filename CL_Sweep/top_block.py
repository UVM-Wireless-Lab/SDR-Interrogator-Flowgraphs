#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CSB Gain Sweep
# Author: Rye Fought (ryesof@gmail.com)
# Description: Script for sweeping C/SB ratio for AM interrogation of harmonic transponder
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import math
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import portable_interrogator_blocks
from gnuradio import uhd
import time
import top_block_getPow as getPow  # embedded python module



from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "CSB Gain Sweep", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("CSB Gain Sweep")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.Stop = Stop = 70
        self.Step = Step = 0.5
        self.Start = Start = 0
        self.RxShift = RxShift = 0.2e6
        self.FTx = FTx = 890e6
        self.samp_rate_src = samp_rate_src = 2e6
        self.path = path = '/home/interrogator/Desktop/Data/Conversion_Loss/'
        self.outlen = outlen = (int(1+(Stop-Start)/Step))
        self.name = name = ''
        self.lpf_cut = lpf_cut = 50e3
        self.buffer = buffer = 10
        self.appendDT = appendDT = True
        self.Sweep = Sweep = False
        self.Length = Length = 1024
        self.GTx = GTx = 0
        self.GRx = GRx = 35
        self.Fm = Fm = 10e3
        self.FRx = FRx = 2*FTx-RxShift
        self.Decimation = Decimation = 20
        self.Average = Average = 2

        ##################################################
        # Blocks
        ##################################################

        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'Configuration')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Rx Signal')
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, 'Sweep Plot')
        self.top_grid_layout.addWidget(self.tab, 2, 0, 1, 4)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._path_tool_bar = Qt.QToolBar(self)
        self._path_tool_bar.addWidget(Qt.QLabel("File Path" + ": "))
        self._path_line_edit = Qt.QLineEdit(str(self.path))
        self._path_tool_bar.addWidget(self._path_line_edit)
        self._path_line_edit.returnPressed.connect(
            lambda: self.set_path(str(str(self._path_line_edit.text()))))
        self.tab_grid_layout_0.addWidget(self._path_tool_bar, 2, 1, 1, 4)
        for r in range(2, 3):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 5):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._outlen_tool_bar = Qt.QToolBar(self)

        if None:
            self._outlen_formatter = None
        else:
            self._outlen_formatter = lambda x: str(x)

        self._outlen_tool_bar.addWidget(Qt.QLabel("Output Length: "))
        self._outlen_label = Qt.QLabel(str(self._outlen_formatter(self.outlen)))
        self._outlen_tool_bar.addWidget(self._outlen_label)
        self.tab_grid_layout_0.addWidget(self._outlen_tool_bar, 3, 6, 1, 2)
        for r in range(3, 4):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._name_tool_bar = Qt.QToolBar(self)
        self._name_tool_bar.addWidget(Qt.QLabel("File Name" + ": "))
        self._name_line_edit = Qt.QLineEdit(str(self.name))
        self._name_tool_bar.addWidget(self._name_line_edit)
        self._name_line_edit.returnPressed.connect(
            lambda: self.set_name(str(str(self._name_line_edit.text()))))
        self.top_grid_layout.addWidget(self._name_tool_bar, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._buffer_tool_bar = Qt.QToolBar(self)
        self._buffer_tool_bar.addWidget(Qt.QLabel("Buffers to discard" + ": "))
        self._buffer_line_edit = Qt.QLineEdit(str(self.buffer))
        self._buffer_tool_bar.addWidget(self._buffer_line_edit)
        self._buffer_line_edit.returnPressed.connect(
            lambda: self.set_buffer(eng_notation.str_to_num(str(self._buffer_line_edit.text()))))
        self.tab_grid_layout_0.addWidget(self._buffer_tool_bar, 1, 2, 1, 2)
        for r in range(1, 2):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        _appendDT_check_box = Qt.QCheckBox("Include Date/Time:")
        self._appendDT_choices = {True: True, False: False}
        self._appendDT_choices_inv = dict((v,k) for k,v in self._appendDT_choices.items())
        self._appendDT_callback = lambda i: Qt.QMetaObject.invokeMethod(_appendDT_check_box, "setChecked", Qt.Q_ARG("bool", self._appendDT_choices_inv[i]))
        self._appendDT_callback(self.appendDT)
        _appendDT_check_box.stateChanged.connect(lambda i: self.set_appendDT(self._appendDT_choices[bool(i)]))
        self.tab_grid_layout_0.addWidget(_appendDT_check_box, 1, 4, 1, 2)
        for r in range(1, 2):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(4, 6):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        _Sweep_check_box = Qt.QCheckBox("Start Sweep:")
        self._Sweep_choices = {True: True, False: False}
        self._Sweep_choices_inv = dict((v,k) for k,v in self._Sweep_choices.items())
        self._Sweep_callback = lambda i: Qt.QMetaObject.invokeMethod(_Sweep_check_box, "setChecked", Qt.Q_ARG("bool", self._Sweep_choices_inv[i]))
        self._Sweep_callback(self.Sweep)
        _Sweep_check_box.stateChanged.connect(lambda i: self.set_Sweep(self._Sweep_choices[bool(i)]))
        self.top_grid_layout.addWidget(_Sweep_check_box, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Stop_tool_bar = Qt.QToolBar(self)

        if None:
            self._Stop_formatter = None
        else:
            self._Stop_formatter = lambda x: eng_notation.num_to_str(x)

        self._Stop_tool_bar.addWidget(Qt.QLabel("Final Gain: "))
        self._Stop_label = Qt.QLabel(str(self._Stop_formatter(self.Stop)))
        self._Stop_tool_bar.addWidget(self._Stop_label)
        self.tab_grid_layout_0.addWidget(self._Stop_tool_bar, 1, 6, 1, 2)
        for r in range(1, 2):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._Step_tool_bar = Qt.QToolBar(self)

        if None:
            self._Step_formatter = None
        else:
            self._Step_formatter = lambda x: eng_notation.num_to_str(x)

        self._Step_tool_bar.addWidget(Qt.QLabel("Step: "))
        self._Step_label = Qt.QLabel(str(self._Step_formatter(self.Step)))
        self._Step_tool_bar.addWidget(self._Step_label)
        self.tab_grid_layout_0.addWidget(self._Step_tool_bar, 2, 6, 1, 2)
        for r in range(2, 3):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._Start_tool_bar = Qt.QToolBar(self)

        if None:
            self._Start_formatter = None
        else:
            self._Start_formatter = lambda x: eng_notation.num_to_str(x)

        self._Start_tool_bar.addWidget(Qt.QLabel("Starting Gain:  "))
        self._Start_label = Qt.QLabel(str(self._Start_formatter(self.Start)))
        self._Start_tool_bar.addWidget(self._Start_label)
        self.tab_grid_layout_0.addWidget(self._Start_tool_bar, 0, 6, 1, 2)
        for r in range(0, 1):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 8):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._GTx_tool_bar = Qt.QToolBar(self)
        self._GTx_tool_bar.addWidget(Qt.QLabel("Transmit Gain" + ": "))
        self._GTx_line_edit = Qt.QLineEdit(str(self.GTx))
        self._GTx_tool_bar.addWidget(self._GTx_line_edit)
        self._GTx_line_edit.returnPressed.connect(
            lambda: self.set_GTx(eng_notation.str_to_num(str(self._GTx_line_edit.text()))))
        self.top_grid_layout.addWidget(self._GTx_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._GRx_tool_bar = Qt.QToolBar(self)
        self._GRx_tool_bar.addWidget(Qt.QLabel("Rx Gain" + ": "))
        self._GRx_line_edit = Qt.QLineEdit(str(self.GRx))
        self._GRx_tool_bar.addWidget(self._GRx_line_edit)
        self._GRx_line_edit.returnPressed.connect(
            lambda: self.set_GRx(eng_notation.str_to_num(str(self._GRx_line_edit.text()))))
        self.tab_grid_layout_0.addWidget(self._GRx_tool_bar, 0, 2, 1, 2)
        for r in range(0, 1):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 4):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._FTx_tool_bar = Qt.QToolBar(self)
        self._FTx_tool_bar.addWidget(Qt.QLabel("Tx Freq" + ": "))
        self._FTx_line_edit = Qt.QLineEdit(str(self.FTx))
        self._FTx_tool_bar.addWidget(self._FTx_line_edit)
        self._FTx_line_edit.returnPressed.connect(
            lambda: self.set_FTx(eng_notation.str_to_num(str(self._FTx_line_edit.text()))))
        self.tab_grid_layout_0.addWidget(self._FTx_tool_bar, 0, 0, 1, 2)
        for r in range(0, 1):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self._Average_tool_bar = Qt.QToolBar(self)
        self._Average_tool_bar.addWidget(Qt.QLabel("Averaging" + ": "))
        self._Average_line_edit = Qt.QLineEdit(str(self.Average))
        self._Average_tool_bar.addWidget(self._Average_line_edit)
        self._Average_line_edit.returnPressed.connect(
            lambda: self.set_Average(int(str(self._Average_line_edit.text()))))
        self.tab_grid_layout_0.addWidget(self._Average_tool_bar, 1, 0, 1, 2)
        for r in range(1, 2):
            self.tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 2):
            self.tab_grid_layout_0.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate_src)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(FRx,0), 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(GRx, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate_src)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(FTx, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(GTx, 0)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            getPow.nextPow(outlen),
            Start,
            Step,
            "Tx Gain [dB]",
            "Tx Gain - PRx [dB]",
            "Relative Conversion Loss",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.01)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 1)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("dB")
        self.qtgui_vector_sink_f_0.set_y_axis_units("dB")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        self.qtgui_vector_sink_f_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [4, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._qtgui_vector_sink_f_0_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (FRx+RxShift), #fc
            (samp_rate_src/Decimation), #bw
            "FFT", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['Source 1', 'Source 2', '', '', '',
            '', '', '', '', '']
        widths = [4, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_freq_sink_x_1_win)
        self.portable_interrogator_blocks_CL_Sweep_Controller_0 = portable_interrogator_blocks.CL_Sweep_Controller(Sweep, Start, Stop, Step, buffer, Average, path, getPow.nextPow(outlen),name,appendDT)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            Decimation,
            firdes.low_pass(
                1,
                samp_rate_src,
                100e3,
                20e3,
                window.WIN_HAMMING,
                6.76))
        self.fft_vxx_0 = fft.fft_vcc(Length, True, window.blackmanharris(Length), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Length)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, Length, 0)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/Length, Length)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_GTx)
        self.blocks_max_xx_1 = blocks.max_ff(Length, 1)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*(-1*(RxShift))/samp_rate_src)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(Length)
        self.analog_sig_source_x_0_2 = analog.sig_source_c(samp_rate_src, analog.GR_CONST_WAVE, Fm, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.portable_interrogator_blocks_CL_Sweep_Controller_0, 'gain_out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.connect((self.analog_sig_source_x_0_2, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_max_xx_1, 0), (self.portable_interrogator_blocks_CL_Sweep_Controller_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_max_xx_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.portable_interrogator_blocks_CL_Sweep_Controller_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_freqshift_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_Stop(self):
        return self.Stop

    def set_Stop(self, Stop):
        self.Stop = Stop
        Qt.QMetaObject.invokeMethod(self._Stop_label, "setText", Qt.Q_ARG("QString", str(self._Stop_formatter(self.Stop))))
        self.set_outlen((int(1+(self.Stop-self.Start)/self.Step)))

    def get_Step(self):
        return self.Step

    def set_Step(self, Step):
        self.Step = Step
        Qt.QMetaObject.invokeMethod(self._Step_label, "setText", Qt.Q_ARG("QString", str(self._Step_formatter(self.Step))))
        self.set_outlen((int(1+(self.Stop-self.Start)/self.Step)))
        self.qtgui_vector_sink_f_0.set_x_axis(self.Start, self.Step)

    def get_Start(self):
        return self.Start

    def set_Start(self, Start):
        self.Start = Start
        Qt.QMetaObject.invokeMethod(self._Start_label, "setText", Qt.Q_ARG("QString", str(self._Start_formatter(self.Start))))
        self.set_outlen((int(1+(self.Stop-self.Start)/self.Step)))
        self.qtgui_vector_sink_f_0.set_x_axis(self.Start, self.Step)

    def get_RxShift(self):
        return self.RxShift

    def set_RxShift(self, RxShift):
        self.RxShift = RxShift
        self.set_FRx(2*self.FTx-self.RxShift)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(-1*(self.RxShift))/self.samp_rate_src)
        self.qtgui_freq_sink_x_1.set_frequency_range((self.FRx+self.RxShift), (self.samp_rate_src/self.Decimation))

    def get_FTx(self):
        return self.FTx

    def set_FTx(self, FTx):
        self.FTx = FTx
        self.set_FRx(2*self.FTx-self.RxShift)
        Qt.QMetaObject.invokeMethod(self._FTx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.FTx)))
        self.uhd_usrp_sink_0.set_center_freq(self.FTx, 0)

    def get_samp_rate_src(self):
        return self.samp_rate_src

    def set_samp_rate_src(self, samp_rate_src):
        self.samp_rate_src = samp_rate_src
        self.analog_sig_source_x_0_2.set_sampling_freq(self.samp_rate_src)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(-1*(self.RxShift))/self.samp_rate_src)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate_src, 100e3, 20e3, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range((self.FRx+self.RxShift), (self.samp_rate_src/self.Decimation))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate_src)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate_src)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
        Qt.QMetaObject.invokeMethod(self._path_line_edit, "setText", Qt.Q_ARG("QString", str(self.path)))
        self.portable_interrogator_blocks_CL_Sweep_Controller_0.set_path(self.path)

    def get_outlen(self):
        return self.outlen

    def set_outlen(self, outlen):
        self.outlen = outlen
        Qt.QMetaObject.invokeMethod(self._outlen_label, "setText", Qt.Q_ARG("QString", str(self._outlen_formatter(self.outlen))))

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        Qt.QMetaObject.invokeMethod(self._name_line_edit, "setText", Qt.Q_ARG("QString", str(self.name)))
        self.portable_interrogator_blocks_CL_Sweep_Controller_0.set_name(self.name)

    def get_lpf_cut(self):
        return self.lpf_cut

    def set_lpf_cut(self, lpf_cut):
        self.lpf_cut = lpf_cut

    def get_buffer(self):
        return self.buffer

    def set_buffer(self, buffer):
        self.buffer = buffer
        Qt.QMetaObject.invokeMethod(self._buffer_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.buffer)))
        self.portable_interrogator_blocks_CL_Sweep_Controller_0.set_buffer(self.buffer)

    def get_appendDT(self):
        return self.appendDT

    def set_appendDT(self, appendDT):
        self.appendDT = appendDT
        self._appendDT_callback(self.appendDT)
        self.portable_interrogator_blocks_CL_Sweep_Controller_0.set_append(self.appendDT)

    def get_Sweep(self):
        return self.Sweep

    def set_Sweep(self, Sweep):
        self.Sweep = Sweep
        self._Sweep_callback(self.Sweep)
        self.portable_interrogator_blocks_CL_Sweep_Controller_0.set_sweep(self.Sweep)

    def get_Length(self):
        return self.Length

    def set_Length(self, Length):
        self.Length = Length
        self.blocks_multiply_const_xx_0.set_k(1/self.Length)

    def get_GTx(self):
        return self.GTx

    def set_GTx(self, GTx):
        self.GTx = GTx
        Qt.QMetaObject.invokeMethod(self._GTx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.GTx)))
        self.uhd_usrp_sink_0.set_gain(self.GTx, 0)

    def get_GRx(self):
        return self.GRx

    def set_GRx(self, GRx):
        self.GRx = GRx
        Qt.QMetaObject.invokeMethod(self._GRx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.GRx)))
        self.uhd_usrp_source_0.set_gain(self.GRx, 0)

    def get_Fm(self):
        return self.Fm

    def set_Fm(self, Fm):
        self.Fm = Fm
        self.analog_sig_source_x_0_2.set_frequency(self.Fm)

    def get_FRx(self):
        return self.FRx

    def set_FRx(self, FRx):
        self.FRx = FRx
        self.qtgui_freq_sink_x_1.set_frequency_range((self.FRx+self.RxShift), (self.samp_rate_src/self.Decimation))
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.FRx,0), 0)

    def get_Decimation(self):
        return self.Decimation

    def set_Decimation(self, Decimation):
        self.Decimation = Decimation
        self.qtgui_freq_sink_x_1.set_frequency_range((self.FRx+self.RxShift), (self.samp_rate_src/self.Decimation))

    def get_Average(self):
        return self.Average

    def set_Average(self, Average):
        self.Average = Average
        Qt.QMetaObject.invokeMethod(self._Average_line_edit, "setText", Qt.Q_ARG("QString", str(self.Average)))
        self.portable_interrogator_blocks_CL_Sweep_Controller_0.set_average(self.Average)




def main(top_block_cls=top_block, options=None):

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
