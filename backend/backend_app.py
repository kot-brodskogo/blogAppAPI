from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.", "author": "Your Name", "date": "2023-06-07"},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "author": "Your Name", "date": "2023-06-07"},
    {"id": 3, "title": "Flask Tutorial", "content": "Learn Flask for web development.", "author": "Your Name", "date": "2023-06-07"},
    {"id": 4, "title": "Python basics", "content": "Introduction to Python programming language.", "author": "Your Name", "date": "2023-06-07"},
]
next_id = 5  # Initially set next available ID


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    if sort_by and sort_by not in ['title', 'content', 'author', 'date']:
        return jsonify({'error': 'Invalid sort field. Use "title" or "content" or "author" or "date".'}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({'error': 'Invalid sort direction. Use "asc" or "desc".'}), 400

    sorted_posts = POSTS.copy()

    if sort_by == 'title':
        sorted_posts.sort(key=lambda post: post['title'], reverse=(direction == 'desc'))
    elif sort_by == 'content':
        sorted_posts.sort(key=lambda post: post['content'], reverse=(direction == 'desc'))
    elif sort_by == 'author':
        sorted_posts.sort(key=lambda post: post['author'], reverse=(direction == 'desc'))
    elif sort_by == 'date':
        sorted_posts.sort(key=lambda post: date.fromisoformat(post['date']), reverse=(direction == 'desc'))

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    global next_id
    global POSTS

    data = request.json
    if not data.get('title') and not data.get('content') and not data.get('author'):
        return jsonify({'error': 'Both title, content and author are required'}), 400
    elif not data.get('title').strip():
        return jsonify({'error': 'Title cannot be empty.'}), 400
    elif not data.get('content').strip():
        return jsonify({'error': 'Content cannot be empty.'}), 400
    elif not data.get('author').strip():
        return jsonify({'error': 'Author cannot be empty.'}), 400

    title = data['title']
    content = data['content']
    author = data['author']
    today = date.today().strftime("%Y-%m-%d")
    post_id = next_id
    next_id += 1

    new_post = {
        'id': post_id,
        'title': title,
        'content': content,
        'author': author,
        'date': today
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS

    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

    return jsonify({'error': f'Post with id {post_id} not found.'}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    global POSTS

    data = request.json

    for post in POSTS:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            if 'author' in data:
                post['author'] = data['author']
            if 'date' in data:
                post['date'] = data['date']
            return jsonify({
                'id': post_id,
                'title': post['title'],
                'content': post['content'],
                'author': post['author'],
                'date': post['date']
            }), 200

    return jsonify({'error': f'Post with id {post_id} not found.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')
    author_query = request.args.get('author')
    date_query = request.args.get('date')

    matched_posts = []
    for post in POSTS:
        if (not title_query or title_query.lower() in post['title'].lower()) and \
           (not content_query or content_query.lower() in post['content'].lower()) and \
           (not author_query or author_query.lower() in post['author'].lower()) and \
           (not date_query or date_query.lower() in post['date'].lower()):
            matched_posts.append(post)

    return jsonify(matched_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
