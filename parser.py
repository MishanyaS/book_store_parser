import requests
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter
import sqlite3
import csv

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9" }

def get_book_url():
    for page in range(1, 4):
        print(f"Page: {page}")
        url = f'https://books.toscrape.com/catalogue/page-{page}.html'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

        for i in data:
            href = i.find('a').get('href')
            book_url = f"https://books.toscrape.com/catalogue/{href}"

            print(f"Book URL: {book_url}")

            yield book_url

def get_books_data():
    counter = 0
    for book_url in get_book_url():
        response = requests.get(book_url, headers=headers)
        sleep(3)
        soup = BeautifulSoup(response.text, 'lxml')

        name = str.strip(soup.find('div', class_='col-sm-6 product_main').find('h1').text)

        price = str.strip(soup.find('div', class_='col-sm-6 product_main').find('p', class_='price_color').text)
        price = price.replace(price[:1], "", 1)

        src = soup.find('div', class_='carousel').find('div', class_='item active').find('img').get('src')
        img = str.strip("https://books.toscrape.com" + src.replace(src[:5], "", 1))

        counter = counter + 1

        print(f"Book №{counter}. Name: {name}, Price: {price}, Image: {img}\n\n")

        yield name, price, img

def write_to_excel(param):
    print("----------WRITING DATA TO XLSX----------")
    book = xlsxwriter.Workbook('books.xlsx')
    page = book.add_worksheet('books')

    row=0
    column=0

    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 50)

    for item in param():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        row+=1

    print("Data about books successfully written to file books.xlsx")

    book.close()

def write_to_db(param):
    print("----------WRITING DATA TO DB----------")
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                  (id INTEGER PRIMARY KEY, name TEXT, price REAL, img TEXT)''')
    cursor.executemany('INSERT INTO books (name, price, img) VALUES (?, ?, ?)', param())

    connection.commit()

    print("Data about books successfully written to DB books.db")

    connection.close()

def write_to_csv():
    file_name = 'books.csv'
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Price', 'Image'])
        
        rows = list(get_books_data())
        writer.writerows(rows)
