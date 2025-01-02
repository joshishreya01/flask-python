from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory databases
books = []
members = []
auth_tokens = {"admin_token": "admin"}

# Helper functions
def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)

def find_member(member_id):
    return next((member for member in members if member['id'] == member_id), None)

def authenticate(request):
    token = request.headers.get('Authorization')
    return token in auth_tokens

@app.route('/books', methods=['GET', 'POST'])
def books_handler():
    # Authentication check
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        # Search and pagination
        title = request.args.get('title', '').lower()
        author = request.args.get('author', '').lower()
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))

        filtered_books = [book for book in books if (title in book['title'].lower() or author in book['author'].lower())]
        start = (page - 1) * per_page
        end = start + per_page
        return jsonify(filtered_books[start:end]), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_book = {
            'id': len(books) + 1,
            'title': data['title'],
            'author': data['author'],
            'published_year': data['published_year'],
            'copies': data['copies']
        }
        books.append(new_book)
        return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_handler(book_id):
    # Authentication check
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'GET':
        return jsonify(book), 200

    elif request.method == 'PUT':
        data = request.get_json()
        book.update(data)
        return jsonify(book), 200

    elif request.method == 'DELETE':
        books.remove(book)
        return jsonify({"message": "Book deleted"}), 200

@app.route('/members', methods=['GET', 'POST'])
def members_handler():
    # Authentication check
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        return jsonify(members), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_member = {
            'id': len(members) + 1,
            'name': data['name'],
            'email': data['email']
        }
        members.append(new_member)
        return jsonify(new_member), 201

@app.route('/members/<int:member_id>', methods=['GET', 'PUT', 'DELETE'])
def member_handler(member_id):
    # Authentication check
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    member = find_member(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    if request.method == 'GET':
        return jsonify(member), 200

    elif request.method == 'PUT':
        data = request.get_json()
        member.update(data)
        return jsonify(member), 200

    elif request.method == 'DELETE':
        members.remove(member)
        return jsonify({"message": "Member deleted"}), 200

@app.route('/auth', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    if data.get('token') in auth_tokens:
        return jsonify({"message": "Authenticated successfully"}), 200
    return jsonify({"error": "Invalid token"}), 403

if __name__ == '__main__':
    app.run(debug=True)
