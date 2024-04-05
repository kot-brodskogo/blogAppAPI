// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.author}</p><p>${post.date}</p><p>${post.content}</p>
                <button class="delete-button" onclick="deletePost(${post.id})">Delete</button>
                <button class="update-button" onclick="updatePost(${post.id})">Update</button>`; // Add an "Update" button
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postAuthor = document.getElementById('post-author').value;
    var postContent = document.getElementById('post-content').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, author: postAuthor, content: postContent })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function updatePost(postId) {
    // This is a placeholder function, will be implemented
}

// Function to send a GET request to the API to search for posts by title or content
function searchPosts() {
    // Retrieve the base URL from the input field
    var baseUrl = document.getElementById('api-base-url').value;

    // Retrieve the search query from the input field
    var searchQuery = document.getElementById('search-query').value;

    // Get selected search types
    var selectedTypes = [];
    document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
        selectedTypes.push(checkbox.value);
    });

    // Construct query URL with multiple search types
    var queryParams = selectedTypes.map(type => `${type}=${searchQuery}`).join('&');
    var url = `${baseUrl}/posts/search?${queryParams}`;

    // Use the Fetch API to send a GET request to the /posts/search endpoint with the search query
    fetch(url)
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.author}</p><p>${post.date}</p><p>${post.content}</p>
                <button class="delete-button" onclick="deletePost(${post.id})">Delete</button>
                <button class="update-button" onclick="updatePost(${post.id})">Update</button>`;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a GET request to the API to sort posts by a specified field
function sortPosts() {
    // Retrieve the base URL from the input field
    var baseUrl = document.getElementById('api-base-url').value;

    // Retrieve the sort field and direction from the input fields
    var sortField = document.getElementById('sort-field').value;
    var sortDirection = document.getElementById('sort-direction').value;

    // Use the Fetch API to send a GET request to the /posts endpoint with the sort parameters
    fetch(`${baseUrl}/posts?sort=${sortField}&direction=${sortDirection}`)
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.author}</p><p>${post.date}</p><p>${post.content}</p>
                <button class="delete-button" onclick="deletePost(${post.id})">Delete</button>
                <button class="update-button" onclick="updatePost(${post.id})">Update</button>`;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

