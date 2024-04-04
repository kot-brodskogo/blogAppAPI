from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
next_id = 3  # Initially set next available ID


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    global next_id

    data = request.json
    if not data.get('title') and not data.get('content'):
        return jsonify({'error': 'Both title and content are required.'}), 400
    elif not data.get('title').strip():
        return jsonify({'error': 'Title cannot be empty.'}), 400
    elif not data.get('content').strip():
        return jsonify({'error': 'Content cannot be empty.'}), 400

    title = data['title']
    content = data['content']
    post_id = next_id
    next_id += 1

    new_post = {
        'id': post_id,
        'title': title,
        'content': content
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
