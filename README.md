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





