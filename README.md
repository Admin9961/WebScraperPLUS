# WebScraperPLUS
Yesterday, after a sleepless night, I failed (accepting defeat) the Instagram bug bounty. The failure was caused by the obligation to manually test the app, not even allowing a passive crawler, resulting in the banning of the guinea pig.

How can one recover from such a miserable defeat?

Following my fateful experience, I developed a humble Python project that allows testing the security of web apps through "botting." This phenomenon, familiar to us all, involves sending automated requests to a website through a script or software.

Tired of the false positives provided by ZAP, its false PII (Private Information Disclosure), its false injection points for imaginary OS command injections, its presumption, and arrogance, and the 500,000 web requests resulting in a best-case scenario DDOS, my "ad-tree" project has a simple purpose: to study the behavior of a website, performing scraping+rendering of HTML, CSS, and JS content. All this with a "full userless" approach, no chromedriver, no geckodriver (pyppeteer is invoked, a Python module that utilizes a similar technique). These programs make our work too easy, preventing us from understanding what a server actually does when it sends HTML, CSS, and Javascript code to us (the client), understanding client/server requests and responses, and the functioning of asynchronous programming, which allows us to manage data flow without generating errors.

In this approach, my bot receives the link of an arbitrary site as input, specified in the format "https://www.example.com," then creates a folder called "downloaded_content" where it downloads the following content:

    The HTML code of the pages hosted by the link, focusing on parsing HTML correctly without neglecting JavaScript and CSS rendering through the requests-html and BeautifulSoup modules. This way, HTML pages are parsed correctly and downloaded without neglecting dynamic changes made by CSS and JavaScript, and the DOM.

    The links of subdirectories belonging to the original link are saved in a file called "link.txt."

    Crawling the site in search of publicly accessible email addresses in the HTML code.

    An external script is called to create a subfolder in "downloaded_content" and save the Javascript code of the page, allowing future inspection. It can be used to understand how Javascript works on websites and to detect vulnerabilities in how the tested web app processes Javascript. In the script, you can adjust the delay to ensure that JS execution is completed in situations where there is more code to process.

    A second external script is called to crawl the images, which are detected through the "img" tag rather than specifying individual extensions, and saved in a second folder named "downloaded_images."

The main file is "parser.py." During its execution, parser.py will automatically call "parse_javascript.py" for JS parsing, while the call to "image_downloader.py" is optional, to give us more control over the type of content we want to download. If you also want to download images, just enter the "guinea pig" link again when prompted by "image_downloader.py." Python 3.7 (minimum) is required for execution, but I worked with Python 3.12.

Now you might wonder, *what does this have to do with the fact that you failed Instagram's bug bounty? From how IG behaved toward ZAP, I deduced that if a web app allows the indiscriminate use of botting, this can pose a risk of DOS, even when the bot's actions are seemingly harmless, as in this case. In fact, my bot does not perform "ignorant" activities like randomly testing SQL injection, OS command injection, XSS, and various other things. However, it uses an insecure scraping practice, as not even a "headless" browser like chromedriver is called to faithfully simulate the behavior of a browser. A less popular variant is used, which can therefore be insecure.

Below, I list a list of websites that allowed scraping by this bot:
Vulnerable sites:

    https://www.google.it (downloaded everything with good rendering)
    https://www.w3.org/contact/ (correctly extracted all email addresses + other contents)
    https://www.qgis.org/en/site/ (although I set as many rules as possible to prevent the bot from getting stuck, something happens here, and at some point, it stops, but it doesn't matter. Because it stops when it has already downloaded everything)

Non-vulnerable sites:

    https://www.inforge.net/forum/forums/sicurezza-informatica.434/ (Cloudflare literally kicked its eyes out, untouchable)

Almost vulnerable sites:

    https://www.instagram.com/This_Profile_is_a_Guinea_Pig (the login page was vulnerable, however, the bot does not support an authentication method, causing rendering and downloading errors after authentication is completed. Still, in my opinion, adding auth support solves the problem)

The script has been successfully tested on Windows; adapting it for Unix may be required. For security reasons, I decided not to compile it with Pyinstaller or Py2exe, providing the code in plain text and 100% commented.
