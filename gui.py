import requests
import re
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from key_contents import query_keywords
import praw
import csv



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
    text = re.sub('<.*?>', '', text)  # Remove HTML tags
    text = text.replace('&gt;', '>')  # Replace &gt; with >
    text = text.replace('&lt;', '<')  # Replace &lt; with <
    text = text.replace('&amp;', '&')  # Replace &amp; with &
    text = text.replace('<br>', '\n')  # Replace <br> with a newline character

    # Remove non-printable characters that are not supported by cp1252 encoding
    text = ''.join(c for c in text if c == '\n' or 32 <= ord(c) <= 126 or c in 'áéíóúÁÉÍÓÚñÑ')

    return text

def display_posts(board):
    islamophobic_posts = fetch_posts(board)

    result_text = ""
    csv_data = [["Name", "Post Content"]]

    for post in islamophobic_posts:
        # Get the name of the user who posted the content
        name = post.get('name', 'Anonymous')
        
        # Clean the post content
        post_content = clean_text(post['com'])

        # Add the cleaned post content to the result text
        result_text += f"{name}: {post_content}\n\n"
        csv_data.append([name, post_content])

    if result_text:
        result_text = f"Islamophobic posts found in /{board}:\n\n{result_text}"
        # Save the data to a CSV file
        with open(f'islamophobic_posts_{board}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_data)
    else:
        result_text = f"No islamophobic posts found in /{board}."

    messagebox.showinfo("Search Results", result_text)


def search_posts(subreddit_name, query, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.search(query, limit=limit)

def utc_to_local(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def on_submit():
    board = entry_board.get()
    display_posts(board)

def on_reddit_submit():
    subreddit_name = entry_subreddit.get()
    limit = entry_limit.get()
    try:
        limit = int(limit)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the limit.")
        return

    search_results = search_posts(subreddit_name, query_keywords, limit)

    result_text = ""
    csv_data = [["Author", "Date Posted", "Title (Short Description)", "Content Link"]]

    for post in search_results:
        author = post.author
        date_posted = utc_to_local(post.created_utc)
        title = post.title
        content_link = post.url
        
        result_text += f"Author: {author}\n"
        result_text += f"Date posted: {date_posted}\n"
        result_text += f"Title (short description): {title}\n"
        result_text += f"Content link: {content_link}\n\n"
        
        csv_data.append([author, date_posted, title, content_link])

    if result_text:
        result_text = f"Reddit search results for /r/{subreddit_name}:\n\n{result_text}"
        # Save the data to a CSV file
        with open(f'reddit_islamophobic_posts_{subreddit_name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_data)
    else:
        result_text = f"No islamophobic posts found in /r/{subreddit_name}."

    messagebox.showinfo("Reddit Search Results", result_text)


def open_about():
    messagebox.showinfo("About", "4chan Islamophobic Post Finder\n\nVersion 1.0.0\n\nCreated by Aslan")

def open_help():
    help_text = """How to use 4chan Islamophobic Post Finder:

1. Enter the 4chan board to monitor (e.g., pol) in the "Board" field.
2. Click the "Submit" button.
3. The application will display a message box with the found islamophobic posts."""

    messagebox.showinfo("Help", help_text)

def exit_app():
    root.destroy()

# Initialize main window
root = tk.Tk()
root.title("Islamophobic Post Finder")
root.geometry("600x400")

# Initialize Reddit API
client_id = '68n97pmuxvLUfkVHxU7w-w'
client_secret = 'bX25ZyAiK9Dg0-h423W5jQkRlDhArw'
user_agent = 'python:islfo:v1.0.0 (by /u/itm448)'
username = 'itm448'
password = 'Chicago12345!'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

# Create menu
menu = tk.Menu(root)
root.config(menu=menu)

help_menu = tk.Menu(menu)
help_menu.add_command(label="Help", command=open_help)
help_menu.add_command(label="About", command=open_about)

# Create tab control (notebook)
tab_control = ttk.Notebook(root)

# Create "4chan Search" tab
tab_4chan_search = ttk.Frame(tab_control)
tab_control.add(tab_4chan_search, text="4chan Search")

# Create "Reddit Search" tab
tab_reddit_search = ttk.Frame(tab_control)
tab_control.add(tab_reddit_search, text="Reddit Search")

# Create "About" tab
tab_about = ttk.Frame(tab_control)
tab_control.add(tab_about, text="About")

tab_control.pack(expand=1, fill="both")

# Add controls to "4chan Search" tab
label_board = ttk.Label(tab_4chan_search, text="Enter the 4chan board to monitor (e.g., pol):")
label_board.grid(row=0, column=0, sticky="e", padx=5, pady=5)

entry_board = ttk.Entry(tab_4chan_search)
entry_board.grid(row=0, column=1, sticky="w", padx=5, pady=5)

submit_button = ttk.Button(tab_4chan_search, text="Submit", command=on_submit)
submit_button.grid(row=1, column=0, columnspan=2, pady=5)

# Add controls to "Reddit Search" tab
label_subreddit = ttk.Label(tab_reddit_search, text="Enter the subreddit to search (e.g., AskReddit):")
label_subreddit.grid(row=0, column=0, sticky="e", padx=5, pady=5)

entry_subreddit = ttk.Entry(tab_reddit_search)
entry_subreddit.grid(row=0, column=1, sticky="w", padx=5, pady=5)

label_limit = ttk.Label(tab_reddit_search, text="Enter the search limit (e.g., 10):")
label_limit.grid(row=1, column=0, sticky="e", padx=5, pady=5)

entry_limit = ttk.Entry(tab_reddit_search)
entry_limit.grid(row=1, column=1, sticky="w", padx=5, pady=5)

reddit_submit_button = ttk.Button(tab_reddit_search, text="Submit", command=on_reddit_submit)
reddit_submit_button.grid(row=2, column=0, columnspan=2, pady=5)

# Add tool description to "About" tab
label_about = ttk.Label(
    tab_about,
    text="Islamophobic Post Finder\n\nVersion 1.0.0\n\nCreated by Aslan\n\nThis tool helps you monitor 4chan boards and Reddit subreddits for islamophobic content.\n\n Enter the board name or subreddit name and click 'Submit' to search for relevant posts.",
    justify="left",
)
label_about.pack(padx=10, pady=10)

root.mainloop()
