import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, book_id):
        book = [b for b in self.books if b["id"] == book_id]
        return book[0] if book else None

    def create(self, data):
        self.books.append(data)
        self.save_all()

    def update(self, book_id, data):
        book = self.get(book_id)
        if not book:
            return False
        index = self.books.index(book)
        self.books[index] = data
        self.save_all()
        return True

    def delete(self, book_id):
        book = self.get(book_id)
        if not book:
            return False
        self.books.remove(book)
        self.save_all()
        return True

    def save_all(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)


books = Books()
