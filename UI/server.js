

const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();
const bodyParser = require('body-parser');

// ENVIRONMENT VARIABLES
const PORT = 50000;
const FRONTEND_URL = "http://localhost:" + PORT

// SETTING UP THE PARSERS
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

// SETTING THE RENDERING ENGINE
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'frontend/views'));

// SETTING THE PUBLIC PATHS
app.use('/js', express.static('frontend/js'));
app.use('/css', express.static('frontend/css'));

// SETTIGN THE RENDERING ENDPOINT
app.get('/', (req, res) => {
  return res.render('index',{
        subject: "FPC Grading Engine", 
    });
});

app.post('/api/process', (req, res) => {
    console.log(req.data, req.body)
    axios({
        method: 'post',
        url: 'http://127.0.0.1:50001/process',
        data: {
            hi:"hello"
        }
      }).then(resp => {
        console.log(resp.data);
        return res.status(200).send(resp.data);
    }).catch(err => {
        console.log('error: ', err)
        return res.status(500).send(err);
    })
   
})


app.listen(PORT, () => {
    console.log(`Webapp is listening on port ${FRONTEND_URL}`);
});