const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();
const path = require('path');

app.use(express.json());
app.use(bodyParser.json());

// Serve your HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Define a route handler for the '/login' endpoint
app.get('/login', (req, res) => {
    // Serve the login page HTML or redirect to the login page URL
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.post('/login', async (req, res) => {
    try {
        const account_number = req.body.account_number;
        const response = await axios.post('http://localhost:5000/login', { account_number });
        // Assuming Flask returns a success message if login is successful
        if (response.data.success) {
            res.redirect('/success');
        } else {
            // If login fails, display an error message on the login page
            res.sendFile(path.join(__dirname, 'login.html'));
        }
    } catch (error) {
        console.error('Error logging in:', error);
        res.status(500).send('Internal Server Error');
    }
});

// Route for creating users
app.post('/api/users', async (req, res) => {
    const { username, email, password } = req.body;
    try {
        // Make a request to your Flask API endpoint to create a user
        const response = await axios.post('http://python-backend:5000/api/user', req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error('Error creating user:', error);
        res.status(error.response ? error.response.status : 500).send(error.message);
    }
});

// Route for updating account information
app.put('/account/:account_id', async (req, res) => {
    try {
        const response = await axios.put(`http://python-backend:5000/api/user/${req.params.account_id}`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.message);
    }
});

// Route for deleting accounts
app.delete('/account/:account_id', async (req, res) => {
    try {
        const response = await axios.delete(`http://python-backend:5000/api/user/${req.params.account_id}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.message);
    }
});

// Start the Express.js server
const port = process.env.PORT || 3004;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
