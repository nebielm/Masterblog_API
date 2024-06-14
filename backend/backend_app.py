from flask import Flask, jsonify, request
from flask_cors import CORS
from random import randint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_book_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.get_json()
    if not validate_book_data(data):
        return jsonify({"error": "Invalid book data"}), 400
    title = data["title"]
    content = data["content"]
    id_is_unique = False
    while not id_is_unique:
        id = randint(1, 1000)
        id_is_unique = True
        for post in POSTS:
            if post['id'] == id:
                id_is_unique = False
                break
    new_post = {"id": id, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify(new_post), 201

def find_post_by_id(id):
    for post in POSTS:
        if post['id'] == id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)
    error_message = {"error": f"Post with id {id} not found."}
    if post is None:
        return jsonify(error_message), 404
    POSTS.remove(post)
    message = {"message": f"Post with id {id} has been deleted successfully."}
    return jsonify(message), 200






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
