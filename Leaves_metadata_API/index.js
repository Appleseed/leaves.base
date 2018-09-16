var express = require('express')
var bodyParser = require('body-parser');
var db = require('./db/db');
var app = express()


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.set('port', process.env.PORT || 8081);
// app.set('host', process.env.HOST || '192.168.99.100');

app.get('/test?:url?:callback', (req, res) => { //returns URL
  fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;
  res.send('ANANT CORPORATION LEAVES API- url: ' + fullUrl + ", ALL METADATA IN CONSOLE.LOG WHEN Index.js is run." + ' url param ' + req.query.url + ' callback ' + req.query.callback); //prints url parameter
});

app.get('/api/v1/todos', (req, res) => {
  res.status(200).send({
    success: 'true',
    message: 'todos retrieved successfully',
    todos: db
  })
});

app.get('/api/v1/todos/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  db.map((todo) => {
    if(todo.id === id) {
      return res.status(200).send({
        success: 'true',
        message: 'todo retrieved successfully',
        todo: todo
      });
    }
  });
});

app.post('/api/v1/todos', (req, res) => {
  if(!req.body.title) {
    return res.status(400).send({
      success: 'false',
      message: 'title is required'
    });
  } else if(!req.body.description) {
    return res.status(400).send({
      success: 'false',
      message: 'description is required'
    });
  }
 const todo = {
   id: db.length + 1,
   title: req.body.title,
   description: req.body.description
 }
 db.push(todo);
 return res.status(201).send({
   success: 'true',
   message: 'todo added successfully',
   todo
 })
});

var leavesApi = require("./leaves.api");
app.get('/content/full?:url', (req, res) => { //first
  //var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  console.log("url " + urlpath);
  leavesApi.leavesContent(urlpath, "FULL HTML", 'JSON', res);
});

app.get('/content/raw?:url', (req, res) => { //first
  //var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  leavesApi.leavesContent(urlpath, "RAW HTML", 'HTML', res);
});

app.get('/content/text?:url', (req, res) => { //first
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  leavesApi.leavesTextCard(urlpath, "TEXT", "TEXT", res);
});

app.get('/meta/card?:url', (req, res) => { //first
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  leavesApi.leavesTextCard(urlpath, "EMBED CARD HTML", "CARD", res);
});

app.get('/images/test?:url', (req, res) => {
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  leavesApi.leavesImages(urlpath, "Default image", '/app/images/imageout_def.png', "", res);
});

app.get('/images/first?:url', (req, res) => { //first
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  var options = {
	  screenSize: {
		width: 320
	  , height: 480
	  }
	, shotSize: {
		width: 320
	  , height: 'all'
	  }
	  }
  leavesApi.leavesImages(urlpath, "First image", '/app/images/imageout.png', options, res);
});

app.get('/images/thumb/large?:url', (req, res) => { //first
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  var options = {
  screenSize: {
    width: 2048
  , height: 898
  }
, shotSize: {
    width: 'all'
  , height: 'all'
  }
  }
  leavesApi.leavesImages(urlpath, "THUMB BIG", '/app/images/imageout-BIG.png', options, res);
});

app.get('/images/thumb/medium?:url', (req, res) => { //first
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  var options = {
  screenSize: {
    width: 1024
  , height: 449
  }
, shotSize: {
    width: 'all'
  , height: 'all'
  }
  }
  leavesApi.leavesImages(urlpath, "THUMB MEDIUM", '/app/images/imageout-MEDIUM.png', options, res);
});

app.get('/images/thumb/small?:url', (req, res) => { //first
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  var options = {
  screenSize: {
    width: 512
  , height: 224
  }
, shotSize: {
    width: 'all'
  , height: 'all'
  }
  }
  leavesApi.leavesImages(urlpath, "THUMB SMALL", '/app/images/imageout-SMALL.png', options, res);
});

app.get('/meta/pagerank?:url', (req, res) => {
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  leavesApi.leavesPageRank(urlpath, "PAGE RANK", res);
});

app.get('/content/read?:url', (req, res) => {
//  var urlpath = 'http://'+req.params.url;
  var urlpath = req.query.url;
  leavesApi.leavesRead(urlpath, "READABLE HTML", res);
});

app.post('/content/read?:url?:callback', (req, res) => {
  var urlpath = 'http://'+req.query.url;
  var callback_url = req.query.callback;
  leavesApi.leavesPost(urlpath, callback_url, "READABLE HTML", req, res);
});

//Note: Embed.ly account costs money

app.listen(app.get('port'), '0.0.0.0', function () {
  //console.log('app listening on port 8081!')
})
