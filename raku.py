#!/usr/bin/env python3
# Raku is a personal assistant chatbot that can run commands, manage tasks, and respond to queries.
# By meinna, 2024.

import tkinter as tk
import subprocess
from responses import chat_responses
from commands import command_map

# Initialize 
root = tk.Tk()
root.title("Raku - Cute Command Chatbot")

window_width = 500
window_height = 400
root.geometry(f"{window_width}x{window_height}")

root.wm_attributes("-topmost", 1)

# Optional: Remove window borders to make it more floating-like (comment out if not needed)
# root.overrideredirect(True)

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

def run_command():
    user_input = entry.get().strip().lower()

    chat_window.insert(tk.END, f"You: {user_input}\n", "user")
    
    if user_input.startswith(('add', 'list', 'delete', 'update')):
        manage_tasks(user_input)
    elif user_input in chat_responses:
        chat_response = chat_responses[user_input]
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
chat_window = tk.Text(root, bg="white", fg="#FF69B4", font=("Comic Sans MS", 10), padx=10, pady=10, wrap="word")
chat_window.pack(expand=True, fill='both', padx=10, pady=10)

entry = tk.Entry(root, bg="#FFE4E1", fg="#FF69B4", font=("Comic Sans MS", 12), bd=5, relief="flat")
entry.pack(fill='x', padx=10, pady=5)

run_button = tk.Button(root, text="✨ Run Command ✨", command=run_command, 
                       bg="#FF69B4", fg="white", font=("Comic Sans MS", 12), 
                       bd=5, relief="raised", padx=10, pady=5)
run_button.pack(fill='x', padx=10, pady=5)

title_label = tk.Label(root, text="Raku - Personal Assistant", bg="#FF69B4", fg="white", font=("Comic Sans MS", 14), pady=10)
title_label.pack(fill='x')

chat_window.tag_config("user", foreground="#FFB6C1") 

# Initialize 
root.mainloop()
