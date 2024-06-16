from flask import Flask, jsonify, request
from flask_cors import CORS
from random import randint

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_book_data(data):
    """checks if "title" and "content" are in data"""
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """handles get request of endpoint '/api/posts' """
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    if sort is None or direction is None:
        return jsonify(POSTS)
    elif sort not in ["title", "content"] or direction not in ["asc", "desc"]:
        return jsonify({"error": "Wrong params provided."}), 400
    sorted_posts = sorted(POSTS, key=lambda post: post[sort])
    if direction == "asc":
        return jsonify(sorted_posts)
    elif direction == "desc":
        return jsonify(sorted_posts[::-1])


@app.route('/api/posts', methods=['POST'])
def add_posts():
    """handles post request of endpoint '/api/posts' """
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
    """checks if given "ID" number is in database"""
    for post in POSTS:
        if post['id'] == id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """handles delete request of endpoint '/api/posts/<int:id>' """
    post = find_post_by_id(id)
    error_message = {"error": f"Post with id {id} not found."}
    if post is None:
        return jsonify(error_message), 404
    POSTS.remove(post)
    message = {"message": f"Post with id {id} has been deleted successfully."}
    return jsonify(message), 200


@app.route("/api/posts/<int:id>", methods=['PUT'])
def update_post(id):
    """handles put request of endpoint '/api/posts/<int:id>' """
    post = find_post_by_id(id)
    error_message = {"error": f"Post with id {id} not found."}
    if post is None:
        return jsonify(error_message), 404
    new_data = request.get_json()
    if not validate_book_data(new_data):
        if 'title' in new_data:
            post["title"] = new_data["title"]
            return jsonify(post)
        elif 'content' in new_data:
            post["content"] = new_data["content"]
            return jsonify(post)
        else:
            return jsonify({"error": "No data provided."}), 400
    post.update(new_data)
    return jsonify(post)


@app.route("/api/posts/search", methods=["GET"])
def query_search():
    """handles get request of endpoint '/api/posts/search' """
    title = request.args.get('title')
    content = request.args.get('content')
    relevant_posts = []
    if title is not None:
        for post in POSTS:
            if title.lower() in post['title'].lower():
                relevant_posts.append(post)
    elif content is not None:
        for post in POSTS:
            if content.lower() in post['content'].lower():
                relevant_posts.append(post)
    return jsonify(relevant_posts)


@app.errorhandler(404)
def not_found_error(error):
    """returns error message 404"""
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """returns error message 405"""
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
