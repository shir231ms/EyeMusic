#!/usr/bin/env node

var fs = require("fs");
var path = require("path");
var browserify = require("browserify");
var args = require('minimist')(process.argv.slice(2));

var b = browserify({ debug: args.debug || false });

var path_to_vexflow = args.path || path.join(__dirname, "node_modules/vexflow/releases/");

console.log(path_to_vexflow);

if (args["include-vexflow"]) {
	b.add(path.join(path_to_vexflow, 'vexflow-debug.js'));
}

b.add('./src/measure.js');
b.add('./src/musicxml.js');
b.add('./src/document.js');
b.add('./src/documentformatter.js');

b.bundle().pipe(fs.createWriteStream("vexflow.musicxml.js"));