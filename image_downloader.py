import os
import asyncio
from urllib.parse import urlparse
from httpx import AsyncClient
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests_html import AsyncHTMLSession

async def download_image(img_url, folder_path):
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

async def download_images(url, folder_path):
    try:
        # Use requests-html to render JavaScript
        session = AsyncHTMLSession()  # Move this line here
        response = await session.get(url)
        await response.html.arender()

        # Introduce a delay after rendering to ensure JavaScript execution is completed
        await asyncio.sleep(2)

        # Extract the HTML content after JavaScript execution
        html_content = response.html.html

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all image tags in the HTML content
        image_tags = soup.find_all('img')

        # Extract and download images with common extensions asynchronously
        tasks = [download_image(urljoin(url, img_tag.get('src')), folder_path) for img_tag in image_tags if img_tag.get('src')]
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Failed to download images: {e}")

    finally:
        # Close the asynchronous HTML session
        await session.close()

async def main():
    # Prompt the user to input the desired website URL
    url = input("Enter the website URL to scrape for images: ")
    folder_path = 'downloaded_images'  # You can change the folder path as needed

    try:
        await download_images(url, folder_path)

    finally:
        pass

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
