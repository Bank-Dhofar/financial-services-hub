const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();
const path = require('path');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.json());

// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve your HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));
});

// Serve the login page
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'login.html'));
});

app.get('/signup', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'signup.html'));
});


// Handle signup form submission
app.post('/signup', async (req, res) => {
    try {
        const { name, balance } = req.body;
        const response = await axios.post('http://127.0.0.1:5001/signup', { name, balance });
        if (response.data.success) {
            res.redirect(`/user-info?account_number=${response.data.account_number}`); // Redirect to user-info page
        } else {
            res.status(400).send(response.data.message); // Show error message
        }
    } catch (error) {
        console.error('Error signing up:', error.message);
        if (error.response) {
            console.error('Error response data:', error.response.data);
            res.status(error.response.status).send(error.response.data);
        } else if (error.request) {
            console.error('No response received:', error.request);
            res.status(500).send('No response received from backend server');
        } else {
            res.status(500).send('Internal Server Error');
        }
    }
});

app.post('/login', async (req, res) => {
    try {
        const account_number = req.body.account_number;
        console.log('Request Body:', req.body);
        
        const response = await axios.post('http://127.0.0.1:5001/login', { account_number });
        console.log('Backend Response:', response.data);

        if (response.data.success) {
            res.json({ success: true });
        } else {
            res.json({ success: false });
        }
    } catch (error) {
        console.error('Error logging in:', error.message);
        if (error.response) {
            console.error('Error response data:', error.response.data);
            res.status(error.response.status).json({ success: false, message: error.response.data });
        } else if (error.request) {
            console.error('No response received:', error.request);
            res.status(500).json({ success: false, message: 'No response received from backend server' });
        } else {
            res.status(500).json({ success: false, message: 'Internal Server Error' });
        }
    }
});

// Route for displaying user info
app.get('/user-info', async (req, res) => {
    try {
        const account_number = req.query.account_number;
        const response = await axios.get(`http://127.0.0.1:5001/user-info?account_number=${account_number}`);
        
        if (response.data.success) {
            res.render('user-info', { user: response.data.user });
        } else {
            res.status(404).json({ success: false, message: 'User not found' });
        }
        
    } catch (error) {
        console.error('Error fetching user info:', error.message);
        if (error.response) {
            console.error('Error response data:', error.response.data);
            res.status(error.response.status).send(error.response.data);
        } else if (error.request) {
            console.error('No response received:', error.request);
            res.status(500).send('No response received from backend server');
        } else {
            res.status(500).send('Internal Server Error');
        }
    }
});


app.get('/generate-report', async (req, res) => {
    try {
        const account_number = req.query.account_number;
        const response = await axios.get(`http://127.0.0.1:5001/generate-report?account_number=${account_number}`, { responseType: 'arraybuffer' });

        res.setHeader('Content-Disposition', 'attachment; filename=report.pdf');
        res.setHeader('Content-Type', 'application/pdf');
        res.send(response.data);
    } catch (error) {
        console.error('Error generating report:', error.message);
        res.status(500).send('Error generating report.');
    }
});


const port = process.env.PORT || 3006;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
    console.log()
});