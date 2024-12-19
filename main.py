from parser import get_books_data, write_to_excel, write_to_db, write_to_csv

if __name__ == '__main__':
    write_to_excel(get_books_data)
    write_to_db(get_books_data)
    write_to_csv()