# VexFlow MusicXML plugin

This is a fork of [@ringw's spectacular fork of VexFlow](https://github.com/ringw/vexflow/tree/musicxml) that adds support for loading MusicXML documents. That effort, which quite successful, is not actively synced with the [upstream repository](https://github.com/0xfe/vexflow), so it does not enjoy the benefits of VexFlow's active development.

Given the difficult of maintaining forks for long periods, this project simply organizes @ringw's contribution as a plugin to the core VexFlow project. I've removed everything except the [files that are specific to the fork](https://github.com/ringw/vexflow/compare/0xfe:master...musicxml).

## Installation

Clone this repo and install the dependencies

	git clone git@github.com:mechanicalscribe/vexflow-musicxml.git && cd vexflow-musicxml
	npm install

This will install VexFlow and a few build dependencies to [node_modules](/node_modules). To build the plugin, just run the build script:

	./build.js --include-vexflow

This will generate a file called [vexflow.musicxml.js](vexflow.musicxml.js). To use it, all you need to do is include it.

	<script src="vexflow.musicxml.js"></script>

After building the script you can see this in action at [demo/index.html](demo/index.html), though you'll need to spin up a server since the page makes an AJAX call to the XML file with the actual music in it:

	python -m SimpleHTTPServer 8080

Then head on over to [localhost:8080/demo/index.html](http://localhost:8080/demo/index.html) for some Moonlight Sonata rendered live in your browser.

## Build options

To skip the VexFlow source and just use this as a plugin, omit `--include-vexflow` in the build:

	./build.js

Then you'd want to do something like:

	<script src="node_modules/vexflow/releases/vexflow-min.js"></script>
	<script src="vexflow.musicxml.js"></script>

To include source maps:

	./build.js --debug

To include Vexflow from somewhere other than `node_modules`:

	./build.js --path=path/to/vexflow/js_file