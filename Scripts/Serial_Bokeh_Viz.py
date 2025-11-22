import serial
import re
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from collections import deque
import time

# Configuration
SERIAL_PORT = 'COM8'  # Initiator COM port (bottom)
BAUD_RATE = 115200
MAX_POINTS = 100 

# Data storage
data_sources = {
    'ifft': ColumnDataSource(data={'time': [], 'ap0': [], 'ap1': [], 'ap2': [], 'ap3': []}),
    'phase_slope': ColumnDataSource(data={'time': [], 'ap0': [], 'ap1': [], 'ap2': [], 'ap3': []}),
    'rtt': ColumnDataSource(data={'time': [], 'ap0': [], 'ap1': [], 'ap2': [], 'ap3': []}),
    'best': ColumnDataSource(data={'time': [], 'ap0': [], 'ap1': [], 'ap2': [], 'ap3': []})
}

# Track which antenna paths are active
active_aps = set()

# Circular buffers for each metric - store as dict by timestamp
buffers = {
    'time': deque(maxlen=MAX_POINTS),
    'ifft': {f'ap{i}': deque(maxlen=MAX_POINTS) for i in range(4)},
    'phase_slope': {f'ap{i}': deque(maxlen=MAX_POINTS) for i in range(4)},
    'rtt': {f'ap{i}': deque(maxlen=MAX_POINTS) for i in range(4)},
    'best': {f'ap{i}': deque(maxlen=MAX_POINTS) for i in range(4)}
}

# Track last values for each AP to fill gaps
last_values = {
    'ifft': {f'ap{i}': None for i in range(4)},
    'phase_slope': {f'ap{i}': None for i in range(4)},
    'rtt': {f'ap{i}': None for i in range(4)},
    'best': {f'ap{i}': None for i in range(4)}
}

start_time = time.time()
pending_ap_data = {}

# Create plots
plots = {}
colors = ['blue', 'red', 'green', 'orange']

for metric in ['ifft', 'phase_slope', 'rtt', 'best']:
    p = figure(title=f'Distance Estimates - {metric.upper()}', 
               x_axis_label='Time (s)', 
               y_axis_label='Distance (m)',
               width=800, height=300)
    
    for i, color in enumerate(colors):
        p.line('time', f'ap{i}', source=data_sources[metric], 
               legend_label=f'AP{i}', color=color, line_width=2)
    
    p.legend.click_policy = "hide"
    plots[metric] = p

# Setup serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Please update SERIAL_PORT in the script")
    exit(1)

# Parse distance log line
# Example: "Distance estimates on antenna path 0: ifft: 1.234, phase_slope: 2.345, rtt: 3.456, best: 1.234"
distance_pattern = re.compile(
    r'Distance estimates on antenna path (\d+): '
    r'ifft: ([-\d.]+), phase_slope: ([-\d.]+), rtt: ([-\d.]+), best: ([-\d.]+)'
)

def parse_distance_line(line):
    """Parse a distance estimate log line"""
    match = distance_pattern.search(line)
    if match:
        ap = int(match.group(1))
        ifft = float(match.group(2))
        phase_slope = float(match.group(3))
        rtt = float(match.group(4))
        best = float(match.group(5))
        return ap, ifft, phase_slope, rtt, best
    return None

def update():
    """Update function called by Bokeh"""
    # Read available lines from serial
    data_updated = False
    current_time = None
    
    while ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                result = parse_distance_line(line)
                if result:
                    ap, ifft, phase_slope, rtt, best = result
                    
                    # Track active APs
                    active_aps.add(ap)
                    
                    # Store in pending data (collect all APs before updating)
                    if current_time is None:
                        current_time = time.time() - start_time
                    
                    if current_time not in pending_ap_data:
                        pending_ap_data[current_time] = {}
                    
                    pending_ap_data[current_time][ap] = {
                        'ifft': ifft,
                        'phase_slope': phase_slope,
                        'rtt': rtt,
                        'best': best
                    }
                    
                    # Update last known values
                    last_values['ifft'][f'ap{ap}'] = ifft
                    last_values['phase_slope'][f'ap{ap}'] = phase_slope
                    last_values['rtt'][f'ap{ap}'] = rtt
                    last_values['best'][f'ap{ap}'] = best
                    
                    data_updated = True
        except Exception as e:
            print(f"Error reading serial: {e}")
            break
    
    # Process pending data if we have complete sets or timeout
    if pending_ap_data and data_updated:
        for timestamp in list(pending_ap_data.keys()):
            # Add time point
            buffers['time'].append(timestamp)
            
            # For each metric, add data for all APs (using last value if not present)
            for metric in ['ifft', 'phase_slope', 'rtt', 'best']:
                for i in range(4):
                    ap_key = f'ap{i}'
                    if i in pending_ap_data[timestamp]:
                        value = pending_ap_data[timestamp][i][metric]
                    else:
                        # Use last known value or NaN
                        value = last_values[metric][ap_key] if last_values[metric][ap_key] is not None else float('nan')
                    buffers[metric][ap_key].append(value)
        
        # Clear pending data
        pending_ap_data.clear()
        
        # Update data sources - ensure all columns have same length
        for metric in ['ifft', 'phase_slope', 'rtt', 'best']:
            time_list = list(buffers['time'])
            new_data = {'time': time_list}
            
            for i in range(4):
                ap_key = f'ap{i}'
                ap_data = list(buffers[metric][ap_key])
                # Ensure same length as time by padding with NaN if needed
                while len(ap_data) < len(time_list):
                    ap_data.append(float('nan'))
                new_data[ap_key] = ap_data[:len(time_list)]  # Truncate if somehow longer
            
            data_sources[metric].data = new_data

# Add update callback
curdoc().add_periodic_callback(update, 100)  # Update every 100ms

# Layout
layout = column(*[plots[m] for m in ['ifft', 'phase_slope', 'rtt', 'best']])
curdoc().add_root(layout)
curdoc().title = "nRF5340 Distance Estimates"