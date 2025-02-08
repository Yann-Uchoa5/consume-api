import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL do site
BASE_URL = "https://books.toscrape.com"

# Função para obter todas as categorias automaticamente
def get_categories():
    response = requests.get(BASE_URL)
    response.encoding = "utf-8"
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        categories = soup.find("ul", class_="nav nav-list").find("ul").find_all("a")
        return {cat.text.strip(): cat["href"] for cat in categories}
    return {}

# Função para obter o número total de páginas de uma categoria
def get_total_pages(category_url):
    response = requests.get(category_url)
    response.encoding = "utf-8"
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pager = soup.find("ul", class_="pager")
        if pager:
            last_page = pager.find("li", class_="current").text.strip().split()[-1]
            return int(last_page)
    return 1

# Função para coletar os livros de uma categoria
def scrape_books(category_name, category_url):
    total_pages = get_total_pages(category_url)
    book_list = []
    for page in range(1, total_pages + 1):
        page_url = category_url.replace("index.html", f"page-{page}.html") if page > 1 else category_url
        response = requests.get(page_url)
        response.encoding = "utf-8"
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        for book in books:
            title = book.h3.a.attrs["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p.attrs["class"][1]
            book_list.append([title, price, rating, category_name])
    return book_list

# Obter todas as categorias do site
categories = get_categories()

# Coletar os dados de todas as categorias
all_books = []
for category_name, category_url in categories.items():
    full_category_url = f"{BASE_URL}/{category_url}"
    books_data = scrape_books(category_name, full_category_url)
    all_books.extend(books_data)

# Criar o DataFrame com os dados
df = pd.DataFrame(all_books, columns=["Título", "Preço", "Classificação", "Categoria"])

# Salvar os dados em um arquivo CSV
df.to_csv("books_by_category.csv", index=False, encoding="utf-8")




import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para obter o número total de páginas de uma categoria
def get_total_pages(base_url, category):
    response = requests.get(f"{base_url}/catalogue/category/books/{category}/index.html")
    response.encoding = "utf-8"
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pager = soup.find("ul", class_="pager")
        if pager:
            # Procurar pela última página
            page_info = pager.find_all("li")[-2].text.strip()  # A última página não está na última posição, mas na penúltima
            last_page = page_info.split()[-1]  # Obter a última palavra, que é o número da página
            return int(last_page)
    return 1

# Função para coletar os livros de uma categoria
def scrape_books(base_url, category):
    total_pages = get_total_pages(base_url, category)
    book_list = []
    for page in range(1, total_pages + 1):
        # Corrigir a URL para incluir o número da página
        url = f"{base_url}/catalogue/category/books/{category}/page-{page}.html"
        response = requests.get(url)
        response.encoding = "utf-8"
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        for book in books:
            title = book.h3.a.attrs["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p.attrs["class"][1]  # A classificação está na segunda classe do <p>
            book_list.append([title, price, rating, category])
    return book_list

# URLs das categorias (corrigido)
categories = [
    "travel_2",
    "mystery_3",
    "historical-fiction_4",
    "sequential-art_5",
    "classics_6",
    "philosophy_7",
    "romance_8",
    "womens-fiction_9",
    "fiction_10",
    "childrens_11",
    "religion_12",
    "nonfiction_13",
    "music_14",
    "default_15",
    "science-fiction_16",
    "sports-and-games_17",
    "add-a-comment_18",
    "fantasy_19",
    "new-adult_20",
    "young-adult_21",
    "science_22",
    "poetry_23",
    "paranormal_24",
    "art_25",
    "psychology_26",
    "autobiography_27",
    "parenting_28",
    "adult-fiction_29",
    "humor_30",
    "horror_31",
    "history_32",
    "food-and-drink_33",
    "christian-fiction_34",
    "business_35",
    "biography_36",
    "thriller_37",
    "contemporary_38",
    "spirituality_39",
    "academic_40",
    "self-help_41",
    "historical_42",
    "christian_43",
    "suspense_44",
    "short-stories_45",
    "novels_46",
    "health_47",
    "politics_48",
    "cultural_49",
    "erotica_50",
    "crime_51"
]

# Base URL
base_url = "https://books.toscrape.com"

# Coletar os dados de todas as categorias
all_books = []
for category in categories:
    print(f"Coletando dados da categoria: {category}")
    books_data = scrape_books(base_url, category)
    all_books.extend(books_data)

# Criar o DataFrame com os dados
df = pd.DataFrame(all_books, columns=["Título", "Preço", "Classificação", "Categoria"])

# Salvar os dados em um arquivo CSV
df.to_csv("books_by_category.csv", index=False, encoding="utf-8")

# Exibir uma mensagem de sucesso
print("Dados extraídos com sucesso!")


# Exibir uma mensagem de sucesso
print("Dados extraídos com sucesso!")
