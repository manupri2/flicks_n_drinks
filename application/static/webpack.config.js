const webpack = require('webpack');

const ExtractTextPlugin = require("extract-text-webpack-plugin");

const config = {
	entry: {
		"indexPage":__dirname + '/js/indexPage.jsx',
		"aboutPage":__dirname + '/js/aboutPage.jsx',
		"CRUDPage":__dirname + '/js/CRUDPage.jsx',
		"stage4Page":__dirname + '/js/stage4Page.jsx',
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
			loader:'babel-loader',
			options:{
				presets:[
					'@babel/preset-env',
                    '@babel/react',{
                    'plugins': ['@babel/plugin-proposal-class-properties']}
				]
			}
		},

		{
			test: /\.css$/,
			use:  ExtractTextPlugin.extract({
				fallback: "style-loader",
				use:"css-loader"
			})
		},
		]
	},

	plugins: [
		new ExtractTextPlugin('styles.css'),
	]

}




module.exports = config;