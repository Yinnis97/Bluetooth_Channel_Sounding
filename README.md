
NOT SURE :
Create a new board this might effect being able to build or not ? who knows...

Create app from example

Add build configuration

build config : 
- Only add base configuration files : prj.config
- Change board to nrf54L15/cpuapp
- Leave the rest empty


blinky sample (zephyr



when picking samples make sure to pick from the zephyr/samples folder.
for channel sounding pick the bluetolth channel sounding connected - Initiator and reflector.

Board : nrf54l15dk/nrf54l15/cpuapp
base configuration file : prj.conf




Important info : https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/bluetooth/channel_sounding/README.rst

NOT SURE ABOUT THIS : We'll most likely have to split them up since all source files are in the same folder so we might have to manually copy the source and include files to our examples
We'll want ot be using the connected_cs example.
And after importing it we'll add the source files and include files manually, make sure to change the makelist when we do this.
 