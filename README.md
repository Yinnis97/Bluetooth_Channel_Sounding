
# **Bluetooth Channel Sounding**

## **Setup**

### Creating a board
 
- We'll be using the nrf54l15.

### Build configuration

1. Create app from example
    - nRF Connect
    - Create a new application
    - Copy a sample (Why wouldn't you)
    - When picking samples make sure to pick from the **nrf** examples.  
    - It's normal for your source files to contain errors, we'll have to add a build configuration first.

2. Add the build configuration

    - nRF Connect
    - U'll have an applications window at the bottom open it.
    - Here you'll have to add a build configuration.
    - This will give you a build config window with certain options.
    - You won't need to change much, only add the following :
        - Only add base configuration files : **prj.conf**
        - Change board to **nrf54l15dk/nrf54l15/cpuapp**
        - Leave the rest empty.
 

## **Distance Methods**

### 1. RTT
**The time it takes for a signal to travel from Initiator → Reflector → back to Initiator**     
1. Initiator sends signal at time T1  
2. Reflector receives at T2, immediately responds   
3. Initiator receives response at T3    

**Distance = (T3 - T1) × speed_of_light / 2**

### 2. Phase Slope (Phase-Based Ranging)

**What it measures:**   
How the phase of the carrier signal changes across different frequencies  

**How it works:**   
Channel Sounding transmits signals on multiple frequencies (channels). As radio waves travel, their phase shifts depending on distance. By comparing phase differences across frequencies, you can calculate distance:  

Signal at frequency f1: phase = φ1  
Signal at frequency f2: phase = φ2  
Signal at frequency f3: phase = φ3  
Phase slope = Δφ / Δf   
**Distance = (phase_slope × speed_of_light) / (2π)**    

**Tip :** Think of it like measuring ripples in a pond at different distances, the pattern tells you how far the wave has traveled.

### 3. IFFT (Inverse Fast Fourier Transform / Frequency Domain)

**What it measures:**   
The channel impulse response – essentially creates a "picture" of all signal paths

**How it works:**   
By transmitting on many different frequencies and analyzing the combined frequency response, IFFT converts this into a time-domain representation showing signal arrivals:


## Extra Information

[Github Repo Nordic : Channel Sounding]( https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/bluetooth/channel_sounding/README.rst)

## Collaborators

[Robert Jansen](https://github.com/jalektro)     
[Niels Franssens](https://github.com/FRniels)   
[Yinnis Kempeneers](https://github.com/Yinnis97)    


