import requests
import re
from key_contents import query_keywords

def is_islamophobic(text):
    for keyword in query_keywords:
        if re.search(keyword, text, re.IGNORECASE):
            print(f"Keyword match: {keyword}")  # Debug information
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

# Ask the user to input the board
board = 'pol'

islamophobic_posts = fetch_posts(board)

for post in islamophobic_posts:
    # Get the name of the user who posted the content
    name = post.get('name', 'Anonymous')
    
    # Clean the post content
    post_content = clean_text(post['com'])

    # Print the user's name along with the cleaned post content
    print(f"{name}: {post_content}")
