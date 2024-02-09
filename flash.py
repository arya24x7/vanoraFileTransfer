import os
import subprocess
import time

def compile_arduino(arduino_ino_path, build_path):
    # Define arduino-cli compile command
    compile_command = [
        "arduino-cli",
        "compile",
        "--fqbn", "arduino:avr:uno",  # Change the board type if needed
        "--build-path", build_path,
        arduino_ino_path
    ]

    try:
        # Compile the Arduino sketch
        subprocess.run(compile_command, check=True)
        print("Compilation completed successfully.")
        return True

    except subprocess.CalledProcessError as e:
        print("Error during compilation:", e)
        return False


def flash_arduino(arduino_port, hex_file_path):
    # Define avrdude command
    avrdude_command = [
        "avrdude",
        "-v",
        "-patmega328p",  # Change the target processor if needed
        "-carduino",
        "-P" + arduino_port,
        "-b115200",  # Change the baud rate if needed
        "-D",
        "-Uflash:w:" + hex_file_path + ":i"
    ]

    try:
        # Flash the Arduino using avrdude
        subprocess.run(avrdude_command, check=True)
        print("Flashing completed successfully.")

    except subprocess.CalledProcessError as e:
        print("Error during flashing:", e)


if __name__ == "__main__":
    # Replace these values with your Arduino port and .ino file path
    arduino_port = "/dev/ttyUSB0"  # Change to the actual port of your Arduino
    arduino_ino_path = "/path/to/your/arduino_sketch.ino"  # Change to the actual path of your .ino file

    # Temporary directory for build files
    build_path = "/tmp/arduino_build"

    # Compile Arduino sketch
    if compile_arduino(arduino_ino_path, build_path):
        # Flash Arduino
        hex_file_path = os.path.join(build_path, "arduino_sketch.ino.hex")
        flash_arduino(arduino_port, hex_file_path)

    # Clean up temporary build directory
    subprocess.run(["rm", "-r", build_path])

