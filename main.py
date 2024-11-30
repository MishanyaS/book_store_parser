from parser import get_books_data, write_to_excel, write_to_db

if __name__ == '__main__':
    write_to_excel(get_books_data)
    write_to_db(get_books_data)