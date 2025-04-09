# SDR-Interrogator-Flowgraphs
## Overview
This repository contains two flowgraphs designed for interrogating harmonic transponders. CL_Sweep performs a single carrier interrogation and monitors the relative conversion loss vs power. AM_Sweep performs a two carrier interrogation using a two tone amplitude modulated (AM) interrogation signal. 

## Requirements
The flowgraphs require the custom blocks in [SDR-Interrogator-Blocks](https://github.com/UVM-Wireless-Lab/SDR-Interrogator-Blocks]). This module must be installed in GNU Radio before running the flowgraphs. 

As they are, these programs will work with USRP B210/200/200mini. Different hardware will require adapting the source/sink blocks in the flowgraphs.

## Running the Flowgraphs
The two flowgraphs (AM_Sweep and CL_Sweep) work very similarly. The fundamental difference between the two is that the AM sweep measures and records four values (carrier to sideband ratio, sideband powers, and carrier power) while the conversion loss sweep only measures one value (the receive power) and records receive power and calculated conversion loss. Otherwise the logic and signal processing is much the same. As such this discussion applies to either program.

![AM_sweep_markup](https://github.com/user-attachments/assets/e935fd0d-da31-4289-b29f-b323ac90c320)

Fig. 1: Annotated flowgraph for AM Sweep


### Setting Sweep Parameters
The sweep parameters are controlled by the GUI Labels outlined in red in Fig. 1. These can not be updated while running because the method used to plot the output data in real time the output vector length must be predetermined at runtime. GNU radio does not allow vector streams to be resized dynamically while running. To set the desired sweep length, set the Start, Stop, and Step values using these GUI Label Blocks.

### GUI Inputs
The purple box in Fig. 1 surrounds the different GUI inputs. These will show up in the GUI on execution as editable parameters (Fig. 2). It may be desireable to alter some of the default values here, for example, the default file path for saving data.

![image](https://github.com/user-attachments/assets/b25cd09f-fc59-4e51-93d9-6bb8d1049058)

Fig. 2: GUI at runtime showing user inputs

### Running a Sweep
To run a power sweep execute the flowgraph. In the GUI window that opens (Fig. 2) enter your desired parameters. PRESS ENTER AFTER ENTERING NEW PARAMETERS, otherwise they will not be updated.

When all the settings are correct, check the "Start Sweep" box to initiate the sweep. You can monitor the received spectrum and look at a plot of the output data using the two other tabs in the GUI. If you uncheck "Start Sweep" while the sweep is executing, the sweep will stop and save the data collected so far. After the sweep has finished, a new sweep can be run by unchecking and then rechecking "Start Sweep"

### Plotting Output Data
The output for the Gain Sweep block is a vector of measured values. To plot this vector in real time, it is fed into the QT GUI Vector Sink block native to GNU radio. To execute efficiently, GNU radio requires the vector length to be a power of two bytes. The parameter "Output Length" in the Gain Sweep block determines this padding. To automatically calculate the minimum appropriate padding from the desired sweep length, the python module "GetPow" (in the teal box in Fig. 1) implements function `int(2**ceil(log2(arg)))`.

Because the output vector is longer than the number of datapoints, the data will not fill the output plot when the sweep is completed. It is possible to zoom in on a desired region by clicking on the plot and dragging to cover the region of interest.

For the AM sweep the live plot shows C/SB vs SDR transmit gain (GTx). For the CL sweep the live plot is GTx-PRx vs GTx; this value is calculated inside the CL sweep block.

### Saving Data
Data is saved as a .csv file to the folder specified by the "Filepath" argument to the sweep controller. The file is saved as `yyyy-mm-dd-HHMMSS_FREQMHz_FileName.csv`. If "Include Date/Time" is not checked in the GUI, the timestamp is omitted. FREQ is the transmit frequency. If the timestamp is not included, the file will be overwritten if duplicate filenames are used.

The format of the .csv is columns organized as `GTx | C/SB | LSB | C | USB` for the AM sweep, where LSB and USB are the lower and upper sideband power and C is the carrier power. For the CL sweep, the file format is `GTx | GTx-PRx | PRx`, where GTx is the SDR Gain and PRx is the measured recieve power.

## Notes
- The receive channel on the SDR is tuned to a frequency slightly off of the second harmonic. A frequency shift is then performed to center the spectrum on the second harmonic, before low pass filtering to reduce the sample rate and eliminate any out of band interference. This is done to avoid a DC spike that can appear on some hardware.
- The modulation frequency used is 10khz. This can be changed by updating the Fm variable
- The transmit amplifier on the B200 series has a maximum gain of 89 dB. However, exceeding ~70 dB begins to introduce nonlinearities from the amplifier. The maximum gain for the receiver amplifier is 76 dB.
- The power measurements providing by the SDR are relative measurements. To get absolute power, a frequency specific calibration should be performed to check the SDR performance at the frequency of interest.

## Contact
Please reach out to sfought@uvm.edu with any questions.







