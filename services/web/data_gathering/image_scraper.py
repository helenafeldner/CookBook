import requests
from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup

def get_image_from_wikipedia(url, name):

    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the image element in the middle of the page
    image_element = soup.find('div', class_='fullImageLink')

    if image_element:
        # Extract the image link
        image_url = 'https:' + image_element.find('a')['href']

        headers = {
        # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'User-Agent': 'Mustafa H. mustafahekmat@hotmail.dk'
        }
        response = requests.get(image_url, headers=headers)

        print('Downloading:', image_url)

        # replace slashes with a dash in the name
        name = name.replace('/', '-')
        # remove the trailing newline
        name = name.strip()

        #get the file extension
        file_extension = image_url.split('.')[-1]
        name = name + '.' + 'png'
        
        # Save the image to a file
        with open('static/images/'+name, 'wb') as f:
            f.write(response.content)
    else:
        print('Image not found on the page.', url)



def get_images_from_list():
    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_high-speed_trains'

    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first table on the page
    table = soup.find('table', class_='wikitable')

    # Find all the rows in the table
    rows = table.find_all('tr')

    # Iterate over the rows and extract the hyperlinks from the 'picture' columns
    for row in rows[2:]:  # Exclude the header row
        # Find the 'picture' column which is the last column in each row
        picture_column = row.find_all('td')
        if picture_column:
            picture_column = picture_column[-1]
        # and name column which is the first column in each row
        name_column = row.find_all('td')
        if name_column:
            name_column = name_column[0]
        
        if picture_column:
            # Find the hyperlink in the 'picture' column
            hyperlink = picture_column.find('a')
            
            if hyperlink:
                # Extract the URL and display it
                picture_url = 'https://en.wikipedia.org' + hyperlink['href']
                get_image_from_wikipedia(picture_url, name_column.text)



if __name__ == '__main__':
    get_images_from_list()