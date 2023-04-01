import requests
from bs4 import BeautifulSoup
'''
# Replace this with the URL of the telegra.ph article you want to extract from
url = "https://telegra.ph/Podruga-08-12"

# Make a request to the URL and get the HTML content
response = requests.get(url)
html_content = response.text
#print(html_content)
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Extract the author name, if available
author = soup.find("a", {"class": "tgme_widget_message_owner_link"})
if author:
    author = author.text

# Extract the publish date, if available
date = soup.find("time", {"class": "published"})
if date:
    date = date.text

# Extract the text of the article
text = ""
article_body = soup.find("article", {"class": "tl_article_content"})
# Extract the title of the article
title = article_body.find("h1").text

if article_body:
    for paragraph in article_body.find_all("p"):
        text += paragraph.text + "\n"
else:
    print("Could not find article body.")

# Print the extracted information
print("Title:", title)
if author:
    print("Author:", author)
if date:
    print("Publish Date:", date)
'''
'''
if text:
    print("Text:", text)

# Print the extracted information
print("Title:", title)
if author:
    print("Author:", author)
if date:
    print("Publish Date:", date)
'''
'''
#print("Text:", text)
from file_manage import write_file_line

#write_file_line('html_content.txt',html_content)
#write_file_line('text_test.txt',text)
#print(text)
charset = str(soup.find('meta'))
charset = charset.split('"')[1]

#print(charset)
f = open('html_content.txt','w',encoding="utf-8")
f.write(html_content)
f.close()
'''


# Replace these with the information for the article you want to upload
access_token = "f8fc053cb1cd38e6d5287146c274fd3ad5d5d65e86f29781cc4411011dae"
title = "Example"
author_name = "Anonymous"
content = "<p>This is the text of the article.</p>"

# Create a dictionary containing the article data
data = {
    "title": title,
    #"author_name": author_name,
    "content": content,
    "access_token": access_token,
    "return_content": True
}

# Make a POST request to the telegra.ph API to upload the article
response = requests.post("https://api.telegra.ph/createPage", data=data)

# Parse the response JSON to get the URL of the uploaded article
url = ''
result = response.json()
if result["ok"]:
    url = "https://telegra.ph/{}".format(result["result"]["path"])
    print("Article uploaded successfully to:", url)
else:
    print("Error uploading article:", result["error"])

path = url
# Make a POST request to the telegra.ph API to edit the article
response = requests.post("https://api.telegra.ph/editPage/{}".format(path), data=data)

# Parse the response JSON to check if the edit was successful
result = response.json()
if result["ok"]:
    print("Article edited successfully.")
else:
    print("Error editing article:", result["error"])