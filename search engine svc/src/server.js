const express = require('express');
const cors = require('cors');
let db_actions = require("./db_actions.js");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.options('*', cors());

app.get('/query/:queryString', (req, res) => {    
    db_actions.GetData(req.params.queryString, function(data){
        res.send(data);
    });
});

app.use(function (req, res) {
    res.status(404).send();
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});