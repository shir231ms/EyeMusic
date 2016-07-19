var express = require("express");
var app = express();
var bodyParser = require('body-parser');

app.all("/index",function(req,res){
	res.redirect("/demo/index.html");
});

app.listen(8080,function () {
  console.log("Start");
});