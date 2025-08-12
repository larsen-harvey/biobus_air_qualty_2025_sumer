import serial
import csv
from datetime import datetime

# === Configuration ===
SERIAL_PORT = 'COM4'        # <-- Change to match your Arduino's port
BAUD_RATE = 115200
CSV_FILE = 'arduino_data1.csv'

# === Open serial connection ===
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Could not open serial port {SERIAL_PORT}: {e}")
    exit(1)

# === Open CSV file and write header ===
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Read header from Arduino
    while True:
        line = ser.readline().decode().strip()
        if line:
            print("Header from Arduino:", line)
            writer.writerow(['Timestamp'] + line.split(','))
            break

    print("Logging data to", CSV_FILE)

    try:
        while True:
            line = ser.readline().decode().strip()
            if line:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                row = [timestamp] + line.split(',')
                print("Logging:", row)
                writer.writerow(row)
    except KeyboardInterrupt:
        print("Logging stopped by user.")
    finally:
        ser.close()
