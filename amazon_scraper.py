import requests
from bs4 import BeautifulSoup

def scrape_amazon_products(url):
  """Scrapes all products from the given Amazon URL.

  Args:
    url: The Amazon product listing URL.

  Returns:
    A list of dictionaries, each containing the product information.
  """

  products = []

  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  product_blocks = soup.find_all("div", class_="s-result-item")
  for product_block in product_blocks:
    product = {}

    product["url"] = product_block.find("a", class_="a-link-normal")["href"]
    product["name"] = product_block.find("span", class_="a-size-base-plus a-color-base a-text-normal").text
    product["price"] = product_block.find("span", class_="a-price").text
    product["rating"] = product_block.find("span", class_="a-icon-alt").text
    product["number_of_reviews"] = product_block.find(
        "span", class_="a-size-base a-color-secondary a-text-normal"
    ).text

    products.append(product)

  return products


def main():
  """Scrapes all products from the given Amazon URL and exports the data in a CSV format.

  Args:
    None.

  Returns:
    None.
  """

  url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
  products = scrape_amazon_products(url)

  with open("amazon_products.csv", "w") as csvfile:
    fieldnames = ["url", "name", "price", "rating", "number_of_reviews"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in products:
      writer.writerow(product)


if __name__ == "__main__":
  main()