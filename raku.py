import tkinter as tk
import subprocess

# Custom command mappings 
command_map = {
    "code": "code",  # Command to open VSCode
    "browser": "firefox",  # Opens Firefox browser
}

# Some simple chat responses
chat_responses = {
    "hello": "Hello!(*^‿^*) How can I help you today?",
    "how are you": "I'm just a bot, but I'm feeling cute! (,,◕///◕,,)",
    "bye": "Goodbye! (∗ᵒ̶̶̷̀ω˂̶́∗)੭₎₎̊₊♡  See you later!",
    "thanks": "You're welcome! ( ˘ ³˘)♥",
}

def run_command():
    user_input = entry.get().strip().lower() 

    if user_input in chat_responses:
        chat_response = chat_responses[user_input]
        chat_window.insert(tk.END, f"Chatbot: {chat_response}\n")
    else:
        command = command_map.get(user_input, user_input)
        
        try:
            subprocess.run(command.split(), check=True)
            chat_window.insert(tk.END, f"~( ˘▾˘~) Ran command: {command}\n")
        except subprocess.CalledProcessError as e:
            chat_window.insert(tk.END, f"⚠️ Error: {str(e)}\n")
    
    entry.delete(0, tk.END)

# The look
root = tk.Tk()
root.title("Cute Command Chatbot")

root.geometry("400x300")
root.config(bg="#FFEBE8")  
root.wm_attributes("-topmost", 1)

chat_window = tk.Text(root, bg="white", fg="#FF69B4", font=("Comic Sans MS", 10)) 
chat_window.pack(expand=True, fill='both', padx=10, pady=10)

entry = tk.Entry(root, bg="#FFE4E1", fg="#FF69B4", font=("Comic Sans MS", 12), bd=5, relief="flat")
entry.pack(fill='x', padx=10, pady=5)

run_button = tk.Button(root, text="✨ Run Command ✨", command=run_command, 
                       bg="#FF69B4", fg="white", font=("Comic Sans MS", 12), 
                       bd=5, relief="raised", padx=10, pady=5)
run_button.pack(fill='x', padx=10, pady=5)

root.mainloop()
