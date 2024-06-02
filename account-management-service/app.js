const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3003;

app.use(express.json());

app.post('/account', async (req, res) => {
    try {
        const response = await axios.post('http://python-backend:5000/account', req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.message);
    }
});

app.put('/account/:account_id', async (req, res) => {
    try {
        const response = await axios.put(`http://python-backend:5000/account/${req.params.account_id}`, req.body);
        res.status(response.status).send(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.message);
    }
});

app.delete('/account/:account_id', async (req, res) => {
    try {
        const response = await axios.delete(`http://python-backend:5000/account/${req.params.account_id}`);
        res.status(response.status).send(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).send(error.message);
    }
});

app.listen(PORT, () => {
    console.log(`Frontend running on port ${PORT}`);
});
