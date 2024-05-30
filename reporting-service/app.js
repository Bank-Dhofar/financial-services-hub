// reporting-service/app.js

const express = require('express');
const bodyParser = require('body-parser');
const postgres = require('pg');

// Initialize express app
const app = express();
app.use(bodyParser.json());

// PostgreSQL database connection
const db = new postgres.Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'reportsdb',
  password: 'password', // Change this to your PostgreSQL password
  port: 5432,
});

// Basic route for testing
app.get('/', (req, res) => {
  res.send('Reporting Service');
});

// Endpoint for generating reports
app.get('/reports', (req, res) => {
  // Reporting logic here
  res.send('Report generated');
});

// Start the server
const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`Reporting Service is running on port ${PORT}`);
});

