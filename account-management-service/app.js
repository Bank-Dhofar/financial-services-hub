const express = require('express');
const mongoose = require('mongoose');
const app = express();
const port = process.env.PORT || 3003;

// MongoDB connection
mongoose.connect('mongodb://mongodb:27017/account-management', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log('Connected to MongoDB');
}).catch(err => {
    console.error('Failed to connect to MongoDB', err);
});

// Middleware to parse JSON requests
app.use(express.json());

// Simple route for the root URL
app.get('/', (req, res) => {
    res.send('Account Management Service');
});

// Define other routes as needed
// app.use('/api/accounts', require('./routes/accounts'));

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});