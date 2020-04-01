const webpack = require('webpack');

const config = {
	entry: {
		"indexPage":__dirname + '/js/indexPage.jsx',
		"aboutPage":__dirname + '/js/aboutPage.jsx'
	},
	output:{
		path: __dirname + '/dist',
		filename: "[name].js"
	},
	resolve: {
		extensions: ['.js', '.jsx', '.css']
	},
	module:{
		rules:[
		{
			test:/\.jsx?/,
			exclude: /node_mocules/,
			use: 'babel-loader'
		}]
	}
};

module.exports = config;