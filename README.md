# Blog API with Flask

📝 This is a simple RESTful API built with Flask that allows users to manage blog posts. Users can perform CRUD (Create, Read, Update, Delete) operations on blog posts through the provided endpoints.

## Features

- ✏️ **Add a new blog post**: Users can create new blog posts.
- ❌ **Delete an existing blog post**: Users can delete their own blog posts.
- 🔄 **Update an existing blog post**: Users can edit their own blog posts.
- 🔍 **Search for posts by title or content**: Users can search for posts containing specific keywords.
- 🔢 **Sort posts based on title or content**: Users can sort posts in ascending or descending order based on title or content.

- 📜 **Pagination** (To be implemented): For blogs with a large number of posts, pagination will be implemented to return a limited number of posts per page.
- 📊 **Expand Data Model** (Future Enhancement): The data model can be expanded to include additional features like comments, categories, or tags.
- 🔑 **User Authorization** (Future Enhancement): User registration and login endpoints can be added, allowing only authenticated users to perform certain actions like creating, updating, and deleting posts.
- ⏳ **Rate Limiting and Versioning** (Future Enhancement): Rate limiting can be implemented to protect the API from abuse, and versioning can be added to plan for future enhancements while maintaining backward compatibility.

## Usage
### Endpoints
- 📬 GET /api/posts: Retrieve all blog posts.
- 📮 POST /api/posts: Add a new blog post.
- 📝 PUT /api/posts/<id>: Update an existing blog post.
- ❌ DELETE /api/posts/<id>: Delete an existing blog post.
- 🔍 GET /api/posts/search: Search for posts by title or content.

### Query Parameters
- 🔄 sort: Specifies the field by which posts should be sorted (title or content).
- 🔢 direction: Specifies the sort order (asc for ascending or desc for descending).

Example:
- To get all posts sorted by title in descending order:
```
GET /api/posts?sort=title&direction=desc
```
- To search for posts containing "Flask" in the title:
```
GET /api/posts/search?title=flask
```

### Request Format
- For adding or updating a post, send a JSON object in the request body with the "title" and "content" fields.

Example:
```json
{
    "title": "New Post",
    "content": "This is a new post."
}
```

## Contributing
🤝 Contributions are welcome! Please fork the repository and submit a pull request with your improvements.