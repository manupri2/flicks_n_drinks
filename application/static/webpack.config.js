const webpack = require('webpack');

const ExtractTextPlugin = require("extract-text-webpack-plugin");

const config = {
	entry: {
		"CRUDPage":__dirname + '/js/CRUDPage.jsx',
		"navigation":__dirname + '/js/navigation.jsx',
		"loginPage":__dirname + '/js/loginPage.jsx',
		"home":__dirname + '/js/home.jsx',
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
