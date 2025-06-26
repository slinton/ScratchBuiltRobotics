from machine import I2C, Pin
import time
import math

# Define I2C Pins (Adjust based on your board)
I2C_SCL = 1  # SCL Pin
I2C_SDA = 0  # SDA Pin

# Initialize I2C
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)

# Magnetometer I2C Address
HMC5883L_ADDR = 0x1E  # Common for HMC5883L
QMC5883L_ADDR = 0x0D  # Common for QMC5883L

# Try detecting the magnetometer
devices = i2c.scan()
if HMC5883L_ADDR in devices:
    MAG_ADDR = HMC5883L_ADDR
    print("HMC5883L detected!")
elif QMC5883L_ADDR in devices:
    MAG_ADDR = QMC5883L_ADDR
    print("QMC5883L detected!")
else:
    print("Magnetometer not found!")
    raise Exception("Check wiring or sensor!")

# Configure HMC5883L
def configure_hmc5883l():
    i2c.writeto_mem(MAG_ADDR, 0x00, b'\x70')  # Set to 8 samples @ 15Hz
    i2c.writeto_mem(MAG_ADDR, 0x01, b'\xA0')  # Set gain
    i2c.writeto_mem(MAG_ADDR, 0x02, b'\x00')  # Continuous measurement mode

# Configure QMC5883L
def configure_qmc5883l():
    i2c.writeto_mem(MAG_ADDR, 0x09, b'\x1D')  # 10Hz, 2G range, continuous mode

# Configure the detected sensor
if MAG_ADDR == HMC5883L_ADDR:
    configure_hmc5883l()
elif MAG_ADDR == QMC5883L_ADDR:
    configure_qmc5883l()

# Read raw magnetometer data
def read_magnetometer():
    if MAG_ADDR == HMC5883L_ADDR:
        data = i2c.readfrom_mem(MAG_ADDR, 0x03, 6)  # Read 6 bytes
        x = (data[0] << 8 | data[1])
        z = (data[2] << 8 | data[3])
        y = (data[4] << 8 | data[5])
    elif MAG_ADDR == QMC5883L_ADDR:
        data = i2c.readfrom_mem(MAG_ADDR, 0x00, 6)  # Read 6 bytes
        x = (data[1] << 8 | data[0])
        y = (data[3] << 8 | data[2])
        z = (data[5] << 8 | data[4])

    # Convert to signed values
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z

    return x, y, z



def calculate_heading(x, y):
    heading_rad = math.atan2(y, x)  # Compute angle in radians
    heading_deg = math.degrees(heading_rad)  # Convert to degrees
    if heading_deg < 0:
        heading_deg += 360  # Ensure positive angle (0 - 360)
    return heading_deg

def calibrate():

    # Initialize variables
    x_min = float('inf')
    x_max = float('-inf')
    y_min = float('inf')
    y_max = float('-inf')

    print("Rotate the magnetometer in all directions for 30 seconds...")
    start_time = time.time()

    while time.time() - start_time < 30:
        x, y, z = read_magnetometer()  # Get raw readings
        
        # Update min/max values
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
        
        print(f"X: {x}, Y: {y}")
        time.sleep(0.1)

    # Compute offsets
    x_offset = (x_max + x_min) / 2
    y_offset = (y_max + y_min) / 2
    
    x_scale = (x_max - x_min) / 2
    y_scale = (y_max - y_min) / 2

    print("\nCalibration complete!")
    print(f"X Offset: {x_offset}, Y Offset: {y_offset}")
    print(f"X Scale: {x_scale}, Y Scale: {y_scale}")
    


# Apply offsets to the magnetometer readings
def read_calibrated_magnetometer():
    x_offset = 2660
    y_offset = 1263
    x_scale = 113
    y_scale = 58
    
    x, y, z = read_magnetometer()
    
    # Apply hard iron correction
    x -= x_offset
    y -= y_offset
    
    # Apply soft iron correction (scaling)
    x /= x_scale
    y /= y_scale
    
    return x, y, z


ALPHA = 0.3  # Smoothing factor (0 < ALPHA ≤ 1, smaller = smoother)

# Initialize values
x_filtered = 0
y_filtered = 0
z_filtered = 0

def read_filtered_magnetometer():
    global x_filtered, y_filtered, z_filtered
    
    x, y, z = read_calibrated_magnetometer()
    
    # Apply exponential moving average
    x_filtered = ALPHA * x + (1 - ALPHA) * x_filtered
    y_filtered = ALPHA * y + (1 - ALPHA) * y_filtered
    z_filtered = ALPHA * z + (1 - ALPHA) * z_filtered
    
    return x_filtered, y_filtered, z_filtered


# Main loop
def main():
    while True:
        #x, y, z = read_magnetometer()
        x, y, z = read_filtered_magnetometer()
        heading = calculate_heading(x, y)
        print(f"Heading: {heading:.2f}°")
        time.sleep(0.1)
        
        
        
#calibrate()
main()


