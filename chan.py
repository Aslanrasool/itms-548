import requests
import re
import tkinter as tk
from tkinter import messagebox
from key_contents import query_keywords

def is_islamophobic(text):
    for keyword in query_keywords:
        if re.search(keyword, text, re.IGNORECASE):
            return True
    return False

def fetch_posts(board):
    url = f'https://a.4cdn.org/{board}/catalog.json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    posts = []
    for page in data:
        for thread in page['threads']:
            if 'com' in thread and is_islamophobic(thread['com']):
                posts.append(thread)

    return posts

def clean_text(text):
    # Clean the text as in the original script
    # ...

def display_posts(board):
    islamophobic_posts = fetch_posts(board)

    result_text = ""
    for post in islamophobic_posts:
        # Get the name of the user who posted the content
        name = post.get('name', 'Anonymous')
        
        # Clean the post content
        post_content = clean_text(post['com'])

        # Add the cleaned post content to the result text
        result_text += f"{name}: {post_content}\n\n"

    if result_text:
        result_text = f"Islamophobic posts found in /{board}:\n\n{result_text}"
    else:
        result_text = f"No islamophobic posts found in /{board}."

    messagebox.showinfo("Search Results", result_text)

def on_submit():
    board = entry_board.get()
    display_posts(board)

root = tk.Tk()
root.title("4chan Islamophobic Post Finder")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_board = tk.Label(frame, text="Enter the 4chan board to monitor (e.g., pol):")
label_board.grid(row=0, column=0, sticky="e")

entry_board = tk.Entry(frame)
entry_board.grid(row=0, column=1)

submit_button = tk.Button(frame, text="Submit", command=on_submit)
submit_button.grid(row=1, column=0, columnspan=2)

root.mainloop()
