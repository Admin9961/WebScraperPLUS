import os
import time
import asyncio
import aiohttp
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import subprocess
from aiohttp import ClientConnectionError, ClientResponseError, ClientPayloadError
from httpx import AsyncClient
import re

print("\nAutore: Christopher Zonta")
print("Email: czonta1996@outlook.it")
print("\nQuesto programma è un bot inteso per lo scraping legale dei siti web. Testato con successo su Google, W3C e 'QGIS.org'. Il test è riuscito in parte anche su Instagram, ma il bot richiede accesso ad un metodo d'autenticazione, che non è stato implementato. Per utilizzare il bot, digita 'pip install -r requirements.txt' navigando con il terminal nella cartella che contiene il progetto. Buona ricerca.\n")
async def download_content(url, folder_path, session, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            # Skip unsupported URLs
            if not url.startswith(('http://', 'https://')):
                print(f"Skipping unsupported URL: {url}")
                return

            # Use requests-html to render JavaScript asynchronously
            response = await session.get(url)
            await response.html.arender(sleep=10)  # Adjust the sleep time as needed

            # Extract the HTML content after JavaScript execution
            html_content = response.html.html

            # Create the 'downloaded_content' directory if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)

            # Extract the file name from the URL
            file_name = os.path.join(folder_path, os.path.basename(urlparse(url).path))

            # Save the rendered HTML content to the specified folder
            with open(file_name + '.html', 'w', encoding='utf-8') as file:
                file.write(html_content)

            print(f"Downloaded: {file_name}.html")
            return

        except (ClientConnectionError, ClientResponseError, ClientPayloadError) as e:
            retries += 1
            print(f"Connection error ({retries}/{max_retries}): {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying

        except Exception as e:
            print(f"Failed to download content: {e}")
            return

    print(f"Max retries exceeded. Failed to download content from: {url}")

async def save_links_to_file(links, folder_path):
    # Save the links to a txt file
    links_file_path = os.path.join(folder_path, 'links.txt')
    with open(links_file_path, 'w', encoding='utf-8') as links_file:
        for link in links:
            links_file.write(f"{link}\n")
    print(f"Links saved in: {links_file_path}")

async def parse_javascript_content(url, folder_path):
    # Call external Python script to parse JavaScript content
    subprocess.run(["python", "parse_javascript.py", url, folder_path])
    subprocess.run(["python", "image_downloader.py"])

async def download_image(img_url, folder_path, session):
    try:
        async with AsyncClient() as client:
            # Use httpx to get the image content asynchronously
            response = await client.get(img_url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Extract the file name from the URL
            img_name = os.path.join(folder_path, os.path.basename(urlparse(img_url).path))

            # Save the image content to the specified folder
            with open(img_name, 'wb') as img_file:
                img_file.write(response.content)

            print(f"Downloaded Image: {img_name}")
    except Exception as e:
        print(f"Failed to download image: {e}")

async def save_to_html(folder_path):
    try:
        # Create a combined HTML file
        combined_html_path = os.path.join(folder_path, 'combined_output.html')
        with open(combined_html_path, 'w', encoding='utf-8') as combined_html_file:
            combined_html_file.write('<html>\n<head>\n<title>Combined Output</title>\n</head>\n<body>\n')

            # Add the HTML content
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as html_file:
                            combined_html_file.write(html_file.read())

            combined_html_file.write('</body>\n</html>')

        print(f"Combined HTML saved in: {combined_html_path}")
    except Exception as e:
        print(f"Failed to create combined HTML: {e}")
        
async def extract_and_save_emails(url, folder_path, session):
    try:
        # Use requests-html to render JavaScript
        response = await session.get(url)
        await response.html.arender()

        # Extract the HTML content after JavaScript execution
        html_content = response.html.html

        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all email addresses using a regular expression
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_regex, soup.get_text())

        # Save the emails to a txt file
        emails_file_path = os.path.join(folder_path, 'emails.txt')
        with open(emails_file_path, 'w', encoding='utf-8') as emails_file:
            for email in emails:
                emails_file.write(f"{email}\n")
        print(f"Emails saved in: {emails_file_path}")

    except Exception as e:
        print(f"Failed to extract and save emails: {e}")

async def main():
    # Prompt the user to input the desired website URL
    url = input("Enter the website URL to scrape: ")

    try:
        # Create an asynchronous HTML session to handle cookies and render JavaScript
        session = AsyncHTMLSession()

        # Open the URL and render JavaScript asynchronously
        response = await session.get(url)
        await response.html.arender()

        # Get the HTML content after JavaScript execution
        html_content = response.html.html

        # Create the 'downloaded_content' directory if it doesn't exist
        folder_path = 'downloaded_content'
        os.makedirs(folder_path, exist_ok=True)

        # Save the HTML, email and CSS content to specified folders asynchronously
        await download_content(url, folder_path, session)
        await extract_and_save_emails(url, folder_path, session)
        
        # Save the content to an HTML file
        html_response_path = os.path.join(folder_path, 'server_response.html')
        with open(html_response_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        print(f"Server Response saved in: {html_response_path}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all links in the HTML content
            all_links = [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href')]

            # Download each content with a delay asynchronously
            tasks = [download_content(link, folder_path, session) for link in all_links]
            await asyncio.gather(*tasks)

            # Save all links to a txt file asynchronously
            await save_links_to_file(all_links, folder_path)

            # Call an external script to parse JavaScript content asynchronously
            await parse_javascript_content(url, folder_path)

            print("Content, links, JavaScript, CSS and pictures parsed and downloaded successfully.")
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    finally:
        # Close the asynchronous HTML session after all tasks are completed
        await session.close()

# Run the asynchronous main function
asyncio.run(main())
