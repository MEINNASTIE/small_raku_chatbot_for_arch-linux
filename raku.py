#!/usr/bin/env python3
# Raku is a personal assistant chatbot that can run commands, manage tasks, and respond to queries.
# By meinna, October 2024.

import tkinter as tk
import subprocess
from tkinter import PhotoImage
from responses import chat_responses
from commands import command_map
from datetime import datetime, timedelta
import random

# Initialize
root = tk.Tk()
root.title("Raku - Cute Command Chatbot")

# Set window dimensions
window_width = 500
window_height = 700
root.geometry(f"{window_width}x{window_height}")

# Make the window float
root.wm_attributes("-topmost", 1)

# Optional: Remove window borders to make it more floating-like
# root.overrideredirect(True)

root.configure(bg="#FFFAF0")

bg_image = PhotoImage(file="/home/meinna/VCS_Projects/small_raku_chatbot_for_arch-linux/kawaii.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Task manager
tasks = []

def manage_tasks(user_input):
    input_split = user_input.split(' ', 2)
    operation = input_split[0]

    if operation == "add" and len(input_split) > 1:
        task = input_split[1]
        tasks.append(task)
        chat_window.insert(tk.END, f"Raku: Task '{task}' added!\n\n")
    
    elif operation == "list":
        if tasks:
            chat_window.insert(tk.END, "Raku: Here are your tasks:\n")
            for i, task in enumerate(tasks):
                chat_window.insert(tk.END, f"{i+1}. {task}\n")
            chat_window.insert(tk.END, "\n")  
        else:
            chat_window.insert(tk.END, "Raku: No tasks available.\n\n")
    
    elif operation == "delete" and len(input_split) > 1:
        try:
            index = int(input_split[1]) - 1
            if 0 <= index < len(tasks):
                removed_task = tasks.pop(index)
                chat_window.insert(tk.END, f"Raku: Task '{removed_task}' deleted!\n\n")
            else:
                chat_window.insert(tk.END, "Raku: Invalid task number.\n\n")
        except ValueError:
            chat_window.insert(tk.END, "Raku: Please provide a valid task number.\n\n")
    
    elif operation == "update" and len(input_split) > 2:
        try:
            index = int(input_split[1]) - 1
            if 0 <= index < len(tasks):
                updated_task = input_split[2]
                tasks[index] = updated_task
                chat_window.insert(tk.END, f"Raku: Task {index+1} updated to '{updated_task}'.\n\n")
            else:
                chat_window.insert(tk.END, "Raku: Invalid task number.\n\n")
        except ValueError:
            chat_window.insert(tk.END, "Raku: Please provide a valid task number.\n\n")
    
    else:
        chat_window.insert(tk.END, "Raku: Invalid task command.\n\n")

def calculate_work_hours(start_time, end_time):
    try:
        start = datetime.strptime(start_time, '%I %p')
        end = datetime.strptime(end_time, '%I %p')

        work_duration = end - start
        if work_duration.total_seconds() < 0:
            work_duration += timedelta(days=1)  
        
        hours, remainder = divmod(work_duration.seconds, 3600)
        minutes = remainder // 60
        return hours, minutes
    except ValueError:
        return None, None

def notify_end_time(end_time):
    current_time = datetime.now().strftime('%I %p')
    current = datetime.strptime(current_time, '%I %p')
    end = datetime.strptime(end_time, '%I %p')

    if end - current <= timedelta(minutes=15):  
        chat_window.insert(tk.END, "Raku: You're almost done with work! Just 15 minutes left.\n\n")

def manage_work_time(user_input):
    input_split = user_input.split(' ', 3)
    if len(input_split) < 4:
        chat_window.insert(tk.END, "Raku: Please provide the correct format: 'work from [start] to [end]'.\n\n")
        return

    start_time = input_split[2]
    end_time = input_split[4]
    hours, minutes = calculate_work_hours(start_time, end_time)

    if hours is not None:
        chat_window.insert(tk.END, f"Raku: You've worked for {hours} hours and {minutes} minutes.\n\n")
        notify_end_time(end_time)
    else:
        chat_window.insert(tk.END, "Raku: Please provide a valid time format (e.g., '8 am' or '3 pm').\n\n")

def run_command():
    user_input = entry.get().strip().lower()

    chat_window.insert(tk.END, f"You: {user_input}\n", "user")
    
    if user_input == "clear":
        chat_window.delete(1.0, tk.END)
        chat_window.insert(tk.END, "Raku: Chat cleared!\n\n")
    elif user_input.startswith(('add', 'list', 'delete', 'update')):
        manage_tasks(user_input)
    elif user_input.startswith('work from'):
        manage_work_time(user_input)
    elif user_input in chat_responses:
        chat_response = random.choice(chat_responses[user_input])
        chat_window.insert(tk.END, f"Raku: {chat_response}\n\n")
    else:
        command = command_map.get(user_input, user_input)
        
        try:
            subprocess.run(command.split(), check=True)
            chat_window.insert(tk.END, f"~( ˘▾˘~) Ran command: {command}\n\n")
        except subprocess.CalledProcessError as e:
            chat_window.insert(tk.END, f"⚠️ Error: {str(e)}\n\n")
    
    entry.delete(0, tk.END)

# GUI Configuration
frame = tk.Frame(root)
frame.pack(expand=True, fill='both', padx=10, pady=10)

title_label = tk.Label(frame, text="Raku - Personal Assistant", bg="#FF69B4", fg="white", font=("Comic Sans MS", 14), pady=10)
title_label.pack(fill='x')

chat_window = tk.Text(frame, bg="white", font=("Comic Sans MS", 10), padx=10, pady=10, wrap="word")
chat_window.pack(expand=True, fill='both', padx=10, pady=5)

entry = tk.Entry(frame, bg="#FFE4E1", fg="#FF69B4", font=("Comic Sans MS", 12), bd=5, relief="flat")
entry.pack(fill='x', padx=10, pady=5)

run_button = tk.Button(frame, text="✨ Run Command ✨", command=run_command, 
                       bg="#FF69B4", fg="white", font=("Comic Sans MS", 12), 
                       bd=5, relief="groove", padx=10, pady=5)
run_button.pack(padx=10, pady=5)

chat_window.tag_config("user", foreground="#FFB6C1") 

# Initialize
root.mainloop()
