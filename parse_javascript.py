import sys
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def extract_javascript_content(url, folder_path):
    try:
        # Create an HTML session to handle cookies and render JavaScript
        session = HTMLSession()

        # Use requests-html to render JavaScript
        response = session.get(url)
        response.html.render()

        # Extract the HTML content after JavaScript execution
        html_content = response.html.html

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all script tags containing JavaScript
        script_tags = soup.find_all('script')

        # Create the 'js_scripts' directory if it doesn't exist
        js_scripts_path = os.path.join(folder_path, 'js_scripts')
        os.makedirs(js_scripts_path, exist_ok=True)

        # Extract and save the JavaScript content to separate .js files
        for i, script_tag in enumerate(script_tags, start=1):
            script_content = script_tag.string
            if script_content:
                js_file_path = os.path.join(js_scripts_path, f'script_{i}.js')
                with open(js_file_path, 'w', encoding='utf-8') as js_file:
                    js_file.write(script_content)
                print(f"JavaScript Content saved in: {js_file_path}\n{'='*30}\n")

    except Exception as e:
        print(f"Failed to extract JavaScript content: {e}")

    finally:
        # Close the HTML session
        session.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_javascript.py [website_url] [folder_path]")
        sys.exit(1)

    website_url = sys.argv[1]
    folder_path = sys.argv[2]

    # Extract and save JavaScript content
    extract_javascript_content(website_url, folder_path)
