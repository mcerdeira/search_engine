const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.options('*', cors());

app.get('/query', (req, res) => {
    res.send("response");
});

// Listen to the App Engine-specified port, or 3000 otherwise
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});