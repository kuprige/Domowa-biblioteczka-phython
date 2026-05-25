from flask import Flask, jsonify, request, abort, make_response
from biblioteka_api.models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "sekretnyklucz"


# ---------------- ERROR HANDLERS ----------------

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        "error": "Not found",
        "status_code": 404
    }), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({
        "error": "Bad request",
        "status_code": 400
    }), 400)


# ---------------- REST API ----------------

@app.route("/api/v1/books/", methods=["GET"])
def books_list():
    return jsonify(books.all())


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or "title" not in request.json:
        abort(400)

    new_book = {
        "id": books.all()[-1]["id"] + 1 if books.all() else 1,
        "title": request.json["title"],
        "author": request.json.get("author", ""),
        "pages": request.json.get("pages", 0),
        "read": request.json.get("read", False)
    }

    books.create(new_book)
    return jsonify({"book": new_book}), 201


@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({"result": True})


@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)

    if not request.json:
        abort(400)

    data = request.json

    if any([
        "title" in data and not isinstance(data["title"], str),
        "author" in data and not isinstance(data["author"], str),
        "pages" in data and not isinstance(data["pages"], int),
        "read" in data and not isinstance(data["read"], bool)
    ]):
        abort(400)

    updated = {
        "id": book_id,
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"]),
        "pages": data.get("pages", book["pages"]),
        "read": data.get("read", book["read"])
    }

    books.update(book_id, updated)
    return jsonify({"book": updated})


if __name__ == "__main__":
    app.run(debug=True)
