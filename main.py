import os
import requests
from bs4 import BeautifulSoup

#Here i created function in order to fetch and manipulate the data from the page
def scrape_animal_data(html_content):
    animals_data = {}
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})
    for table in tables:
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) >= 7:
                animal_cell = columns[0]
                if table == tables[0]:
                    collateral_adjective_cell = columns[6]
                else:
                    collateral_adjective_cell = columns[5]

                animal_links = animal_cell.find_all("a")
                animal_names = [link.get_text() for link in animal_links]

                collateral_adjective_text = collateral_adjective_cell.get_text(strip=True)
                collateral_adjective = collateral_adjective_text.split("(")[0].strip()

                if collateral_adjective:
                    if collateral_adjective not in animals_data:
                        animals_data[collateral_adjective] = []
                    animals_data[collateral_adjective].extend(animal_names)
    return animals_data

#Here i download the images
def download_images(animals_data, image_dir):
    os.makedirs(image_dir, exist_ok=True)
    for collateral_adjective, animals in animals_data.items():
        for animal in animals:
            animal_page_url = f"https://en.wikipedia.org/wiki/{animal.replace(' ', '_')}"
            animal_page_response = requests.get(animal_page_url)
            animal_page_soup = BeautifulSoup(animal_page_response.content, "html.parser")

            possible_classes = ["image", "thumbimage"]
            image_link = None
            for class_name in possible_classes:
                image_element = animal_page_soup.find("a", {"class": class_name})
                if image_element and image_element.find("img"):
                    image_link = image_element.find("img")["src"]
                    break

            if image_link:
                image_url = f"https:{image_link}"
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_filename = os.path.join(image_dir, f"{animal}.jpg")
                    with open(image_filename, "wb") as image_file:
                        image_file.write(image_response.content)

#Here i generate the html content
def generate_html(animals_data, image_dir):
    html_output = "<html>\n<body>\n"
    for collateral_adjective, animals in animals_data.items():
        html_output += f"  <h2>Collateral Adjective: {collateral_adjective}</h2>\n"
        for animal in animals:
            image_filename = f"{image_dir}/{animal}.jpg"  # Use relative path
            html_output += f'  <p><img src="{image_filename}" alt="{animal}"> - {animal}</p>\n'
    html_output += "</body>\n</html>"
    return html_output

url = "https://en.wikipedia.org/wiki/List_of_animal_names"
response = requests.get(url)
html_content = response.content
animals_data = scrape_animal_data(html_content)

image_dir = "animal_images"  # Relative path

download_images(animals_data, image_dir)
html_output = generate_html(animals_data, image_dir)


