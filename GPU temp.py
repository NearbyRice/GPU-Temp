import subprocess
import time
import pygame
import tkinter as tk
from tkinter import messagebox
import os

# Function to get GPU temperature using nvidia-smi
def get_gpu_temperature():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'], stdout=subprocess.PIPE)
        temperature = int(result.stdout.decode().strip())
        return temperature
    except Exception as e:
        print("Error:", e)
        return None

# Function to play audible tone
def play_tone():
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(os.getcwd(), 'GPU Temp' '\warning_tone.wav')) 
    pygame.mixer.music.play()
    pygame.quit

# Function to display warning notification
def show_warning_notification(temperature):
    root = tk.Tk()
    root.withdraw()
    
    messagebox.showwarning("Warning", "GPU temperature is approaching temperture limit! Temp: "+str(temperature))

# Function to display info box and power off the system
def power_off_system():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Info", "This system will power off in 90 seconds. Please save any unsaved progress.")
    time.sleep(90)
    # power off the system after 90 seconds
    print("Shutting Down System")
    messagebox.showinfo("Info", "Shutting Down!")
    play_tone()
    os.system("shutdown /s /t 0")

# Main function
def main():
    play_tone()
    warning_limit = 87  # Set your warning limit
    temperature_limit = 92  # Set your temperature limit

    while True:
        temperature = get_gpu_temperature()
        if temperature is not None:
            print("GPU Temperature:", temperature)
            if temperature >= warning_limit:
                play_tone()
                show_warning_notification(temperature)
            if temperature >= temperature_limit:
                play_tone()
                power_off_system()
                break  # Exit the loop and power off the system
        time.sleep(10)  # Check temperature every 30 seconds

if __name__ == "__main__":
    main()
