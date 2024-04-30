const express  = require('express');
const http = require('http');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
const PORT = 8080;


app.get('/', (req, res) => {
    console.log("Received GET request");
    console.log(req.url);
    res.status(200).send(req.query['hub.challenge']);
});

app.get('/protochat', (req, res) => {
    console.log("Received GET request");
    console.log(req.url);
    res.status(200).send(req.query['hub.challenge']);
});

app.post('/protochat', (req, res) => {
    if (req.body.entry[0].changes[0].value.messages == undefined){
        console.log("Received empty POST request");
        console.log(req.body.entry[0].changes[0].value.statuses)
        res.status(200).send('OK');
        return;
    }
    var postData = JSON.stringify({
        "celnumber": req.body.entry[0].changes[0].value.messages[0].from,
        "question": req.body.entry[0].changes[0].value.messages[0].text.body
    });
    console.log(postData);
    var options = {
        hostname: 'localhost',
        port: 8000,
        path: '/leila',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };
    var r = http.request(options, (res) => {
        console.log(`statusCode: ${res.statusCode}`);
        res.setEncoding('utf8');
        res.on('data', (d) => {
            console.log(d);
        });
    });

    r.on('error', (error) => {
        console.error(error);
    });

    r.write(postData);
    r.end();
    res.status(200).send('OK');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});