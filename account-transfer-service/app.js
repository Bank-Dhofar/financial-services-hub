const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

// Initialize express app
const app = express();
app.use(bodyParser.json());

// MySQL database connection
const db = mysql.createConnection({
  host: 'mysql',
  user: 'root',
  password: 'password', // Change this to your root password
  database: 'transferdb'
});

// Connect to MySQL
db.connect(err => {
  if (err) {
    console.error('Database connection failed: ' + err.stack);
    return;
  }
  console.log('Connected to MySQL database');
});

// Basic route for testing
app.get('/', (req, res) => {
  res.send('Account Transfer Service');
});

// Endpoint for transferring funds
app.post('/transfer', (req, res) => {
  const { fromAccount, toAccount, amount } = req.body;

  // Ensure all necessary data is provided
  if (!fromAccount || !toAccount || !amount) {
    return res.status(400).send('Missing required fields');
  }

  // Transfer logic here
  db.beginTransaction(err => {
    if (err) { throw err; }
    db.query('UPDATE accounts SET balance = balance - ? WHERE id = ?', [amount, fromAccount], (error, results, fields) => {
      if (error) {
        return db.rollback(() => {
          throw error;
        });
      }

      db.query('UPDATE accounts SET balance = balance + ? WHERE id = ?', [amount, toAccount], (error, results, fields) => {
        if (error) {
          return db.rollback(() => {
            throw error;
          });
        }

        db.commit(err => {
          if (err) {
            return db.rollback(() => {
              throw err;
            });
          }
          res.send('Transfer successful');
        });
      });
    });
  });
});

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Account Transfer Service is running on port ${PORT}`);
});
