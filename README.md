
# Bluetooth Channel Sounding

## Setup

### Creating a board

- Create a new board for future use, not sure if this is neccesary.   
- We'll be using the nrf54l15.

### Build configuration

1. Create app from example
    - nRF Connect
    - Create a new application
    - Copy a sample (Why wouldn't you)
    - When picking samples make sure to pick from the zephyr/samples folder.    
        For some reason the nrf folder ends up with tons of build errors, cba to figure it out.
    - It's normal for your source files to contain errors, we'll have to add a build configuration first.

2. Add the build configuration

    - nRF Connect
    - U'll have an applications window at the bottom open it.
    - Here you'll have to add a build configuration.
    - This will give you a build config window with certain options.
    - You won't need to change much, only add the following :
        - Only add base configuration files : **prj.conf**
        - Change board to **nrf54l15dk/nrf54l15/cpuapp**
        - Leave the rest empty

3. Extra

    - We'll have to delete the source files that are not needed, because for some reason it loads all of them instead of only the ones we need.
    - We'll want to be using the **connected_cs** example (for more info read the nordic readme).
 
## Extra Information

[Github Repo Nordic : Channel Sounding]( https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/bluetooth/channel_sounding/README.rst)

## Collaborators

[Robert Jansen](https://github.com/jalektro)     
[Niels Franssens](https://github.com/FRniels)   
[Yinnis Kempeneers](https://github.com/Yinnis97)    
