from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS_FILE = "posts.json"


# Function to read posts from the JSON file
def read_posts():
    try:
        with open(POSTS_FILE, "r") as file:
            posts = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        posts = []
    return posts


# Function to write posts to the JSON file
def write_posts(posts):
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_by = request.args.get('sort')
    direction = request.args.get('direction')

    if sort_by and sort_by not in ['title', 'content', 'author', 'date']:
        return jsonify({'error': 'Invalid sort field. Use "title" or "content" or "author" or "date".'}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({'error': 'Invalid sort direction. Use "asc" or "desc".'}), 400

    sorted_posts = read_posts().copy()

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
    data = request.json

    if not data.get('title') and not data.get('content') and not data.get('author'):
        return jsonify({'error': 'Both title, content and author are required'}), 400
    elif not data.get('title').strip():
        return jsonify({'error': 'Title cannot be empty.'}), 400
    elif not data.get('content').strip():
        return jsonify({'error': 'Content cannot be empty.'}), 400
    elif not data.get('author').strip():
        return jsonify({'error': 'Author cannot be empty.'}), 400

    # If all checks pass, proceed to add the post
    posts = read_posts()
    today = date.today().strftime("%Y-%m-%d")
    # Generate a unique index for the new post
    if posts:
        new_index = max(post['id'] for post in posts) + 1
    else:
        new_index = 1

    new_post = {
        'id': new_index,
        'title': data['title'],
        'content': data['content'],
        'author': data['author'],
        'date': today
    }

    posts.append(new_post)
    write_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    posts = read_posts()

    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            write_posts(posts)
            return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

    return jsonify({'error': f'Post with id {post_id} not found.'}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    posts = read_posts()

    for post in posts:
        if post['id'] == post_id:
            if 'title' in data:
                post['title'] = data['title']
            if 'content' in data:
                post['content'] = data['content']
            if 'author' in data:
                post['author'] = data['author']
            if 'date' in data:
                post['date'] = data['date']

            # Update the JSON file with the modified posts
            write_posts(posts)

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
    posts = read_posts()
    title_query = request.args.get('title')
    content_query = request.args.get('content')
    author_query = request.args.get('author')
    date_query = request.args.get('date')

    matched_posts = []
    for post in posts:
        if (not title_query or title_query.lower() in post['title'].lower()) and \
           (not content_query or content_query.lower() in post['content'].lower()) and \
           (not author_query or author_query.lower() in post['author'].lower()) and \
           (not date_query or date_query.lower() in post['date'].lower()):
            matched_posts.append(post)

    return jsonify(matched_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
