import os
import time
import subprocess
import random
from colorama import Fore, init
import sys

init(autoreset=True)

def flash_message(message, flash_duration=1, flash_interval=0.5, color=Fore.RED):
    end_time = time.time() + flash_duration
    while time.time() < end_time:
        rows, cols = os.popen('stty size', 'r').read().split()  
        rows, cols = int(rows), int(cols)
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - len(message))
        print(f"\033[{random_row};{random_col}H{color + message}", end='', flush=True)
        time.sleep(flash_interval)
        print("\033[K", end='', flush=True)  
        time.sleep(flash_interval)

def display_ascii_art():
    ascii_art = """ 
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣤⣄⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣻⣿⣿⣿⣿⣿⣿⣿⠉⠉⠛⠛⠛⠛⠿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠲⠶⢤⡄⠀⠘⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⡿⠁⣂⡀⠀⠀⠀⠀⠀⠦⠤⣽⠷⣾⢷⢮⣀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⡷⠟⠉⠀⠀⢀⣠⣶⣶⣶⣤⣠⣤⡟⠈⢻⡿⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠠⠼⠿⢻⣿⣻⣿⣿⣿⣿⣿⣷⣾⣣⣇⡀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⢿⡿⣿⣿⣿⠁⠀⠀⠀⠲⣶⣷⣿⣿⣿⣿⣿⣿⣿⠟⢻⣟⣿⣿⣿⣾⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠃⡼⣁⢀⣿⠁⠀⠀⠀⠀⠀⠉⠙⢿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣭⣛⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡟⠻⡟⣿⣷⡆⠀⠀⠀⠀⠀⢀⣠⣬⣿⣿⣿⣿⡋⠀⠈⢻⣟⣿⣌⣻⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⢷⣤⢁⣿⡿⣿⣀⣀⢀⡀⣼⠿⠟⢋⣿⣿⣿⣯⢉⣓⣂⠈⣿⠙⣿⠉⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⣤⡷⣾⣿⠷⢻⣿⣷⣿⣿⡟⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣼⣷⠀⣼⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢀⣿⠛⣷⣴⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠗⢿⣽⡏⣸⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢸⣿⣟⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢶⣿⣏⣙⡋⢳⣦⣿⣵⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣽⣿⣿⡊⢹⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠉⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⡃⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠈⠹⠻⣿⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⠶⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣀⣤⡶⠖⠛⠛⠉⠉⣁⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⣿⣿⡿⠉⠁⢸⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣤⣶⠿⠛⠉⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⢰⣾⣿⡷⠀⠀⣾⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠟⠁⠀⠀⠃⢀⠈⠉⢁⣨⣭⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡇⠀⣀⣿⣿⡏⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡀⠀⠠⠆⠒⣿⣶⣾⣿⣿⣿⡿⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀⣿⣿⡏⠀⢸⠁⠀⡙⠷⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣶⣦⣶⣿⣿⣿⣿⣿⣿⣿⣧⣥⣄⡀⠀⠀⠀⣄⣀⠀⠀⡀⠀⠀⠀⣿⣿⣿⢿⣿⢀⣴⡻⠀⠀⣧⠀⠀⠈⠛⠶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣷⣄⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠛⠛⠿⠿⠿⣿⣷⣶⣿⣄⠀⢰⣿⢻⣿⣸⣿⣾⠁⠁⠇⠀⢿⣷⡤⣄⣀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠻⠿⣿⣧⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⣀⠀⠈⠉⠙⠿⠷⣿⣏⠀⣿⣿⣿⡇⠀⠈⡀⠀⠈⠻⣷⡈⠻⢿⣤⠀⠈⠻⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠉⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡋⠀⠉⠠⠀⠈⠻⣄⢹⣿⡟⢀⣀⡴⢿⣶⠒⠺⠟⠛⠂⠀⢻⡆⢰⣶⣬⣍⣉⠓⠶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⠀⠀⠂⠶⢤⣄⡙⠀⠻⠁⣾⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣾⣿⣿⡟⠋⠙⠓⠂⠙⠓⠒⠶⢤⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⠶⠀⠈⠀⠒⠀⢺⣿⣷⣿⣙⡻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣷⣀⢤⡴⢄⠀⠀⠀⠀⠀⠀⠉⠳⠦⣄⠀⠀⠀
⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠀⠀⠘⣿⣿⡿⣿⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣯⣷⣘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀
⠴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠳⣄⠀⢸⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻
⠀⠀⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠄⠀⠀⠙⠀⢸⣿⣿⣿⠀⠀⠀⠀@CHOROZON⠀⠀⠀⠀⠀⠀⠀⠉⣹⣿⠷⣦⣁⠂⠀⠀⠀⠀⠀⠀
⠤⠄⠀⠀⠀⣀⡀⢀⡀⠤⠀⠉⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣦⠈⠛⢷⣄⠀⠀⠀⠀⠀
⠛⠀⠀⠀⠀⠀⠠⠄⢀⡀⢀⣤⢠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⠀⠈⠙⠀⠀⠀⠀⠀
⠀⠀⠀⣐⣂⣀⣀⠀⣶⣶⣾⢉⣴⢾⣿⣷⣤⣤⣤⣤⣠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡄⢀⣀⠀⠄⠈⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣦⡀⣀⣀⣀⣀⠀⢀ 
    """
    print(ascii_art)  

def typewriter_effect(message, delay=0.1):
    for char in message:
        print(char, end='', flush=True)  
        time.sleep(delay)  
    print()  

def display_next_message(message, delay=0.5):
    time.sleep(delay)  
    print(message)

def run_chad_script():
    try:
        process = subprocess.Popen(['python3', 'chad.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        output_buffer = []

        def update_output_buffer(new_line):
            if len(output_buffer) >= 5:
                output_buffer.pop(0)  
            output_buffer.append(new_line)  
            clear_screen_below_ascii()
            for line in output_buffer:
                print(line, end='')

        line_count = 0
        for line in process.stdout:
            update_output_buffer(line)

        for line in process.stderr:
            update_output_buffer(Fore.RED + line)

        process.wait()  

    except Exception as e:
        print(Fore.RED + f"Error running chad.py: {e}")

def run_sql_pwn_script():
    try:
        process = subprocess.Popen(['python3', 'sql.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        output_buffer = []

        def update_output_buffer(new_line):
            if len(output_buffer) >= 5:
                output_buffer.pop(0)  
            output_buffer.append(new_line)  
            clear_screen_below_ascii()
            for line in output_buffer:
                print(line, end='')

        line_count = 0
        for line in process.stdout:
            update_output_buffer(line)

        for line in process.stderr:
            update_output_buffer(Fore.RED + line)

        process.wait()  

    except Exception as e:
        print(Fore.RED + f"Error running sql.py: {e}")

def go_back_to_menu():
    print("\nReturning to menu...\n")
    time.sleep(2)  

def clear_screen_below_ascii():
    os.system('cls' if os.name == 'nt' else 'clear')  
    display_ascii_art()  

def main():
    while True:  
        flash_message("Привет", flash_duration=2, flash_interval=0.3, color=Fore.RED)
        clear_screen_below_ascii()
        typewriter_effect("Welcome to CHAD - Dork Pentesting Tool @CHOROZON ", delay=0.1)
        display_next_message("CHOOSE YOUR OPTION")
        flash_message("CHOOSE YOUR OPTION", flash_duration=1, flash_interval=0.5)
        user_input = input("Enter your option: ").strip().lower()  

        clear_screen_below_ascii()

        if user_input == "-wp-pawn":
            run_chad_script()
            go_back_to_menu()
        
        elif user_input == "sql-pwn":
            run_sql_pwn_script()
            go_back_to_menu()
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

