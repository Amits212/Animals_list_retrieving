import os
import pytest
from main import scrape_animal_data, download_images, generate_html

@pytest.fixture
def sample_html_content():
    with open("sample.html", "r", encoding="utf-8") as file:
        return file.read()

def test_scrape_animal_data(sample_html_content):
    animals_data = scrape_animal_data(sample_html_content)
    assert "avian" in animals_data
    assert "hippotigrinezebrine" in animals_data

def test_download_images(tmpdir):
    animals_data = {
        "Collateral 1 (adj)": ["Aves"],
        "Collateral 2 (adj)": ["Zebra"]
    }
    image_dir = tmpdir.mkdir("animal_images")
    download_images(animals_data, str(image_dir))
    assert len(os.listdir(image_dir)) == 2

def test_generate_html(tmpdir):
    animals_data = {
        "Collateral 1 (adj)": ["Aves"],
        "Collateral 2 (adj)": ["Zebra"]
    }
    image_dir = tmpdir.mkdir("animal_images")
    html_output = generate_html(animals_data, str(image_dir))
    assert "<h2>Collateral Adjective: Collateral 1 (adj)</h2>" in html_output
    assert '<img src="animal_images/Aves.jpg" alt="Aves"> - Aves' in html_output
    assert '<img src="animal_images/Zebra.jpg" alt="Zebra"> - Zebra' in html_output
