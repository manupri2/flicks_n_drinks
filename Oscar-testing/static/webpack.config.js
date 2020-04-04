const webpack = require('webpack');
const ExtractTextPlugin = require("extract-text-webpack-plugin");


const config = {
	entry: {
		"indexPage":__dirname + '/js/indexPage_WS.jsx',
		"aboutPage":__dirname + '/js/aboutPage.jsx',
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
			exclude: /node_modules/,
			loader:'babel-loader'
			// loader: 'babel-loader',
			// options:{
			// 	presets:[
			// 		"@babel/preset-env",
			// 		"@babel/preset-react"
			// 	],
			// 	plugins:[
			// 		"@babel/plugin-syntax-dynamic-import",
			// 		"@babel/transform-runtime",
			// 		"@babel/plugin-proposal-class-properties"
			// 	]
			// }


		},

		{
			test: /\.css$/,
			loader:  ExtractTextPlugin.extract({
				fallback: "style-loader",
				use:"css-loader"
			})
		},
		
		// {
		// 	test:/\.js/,
		// 	loader: "babel-loader",
		// 	options:{
		// 		presets:[
		// 			"@babel/preset-env",
		// 			"@babel/preset-react"
		// 		],
		// 		plugins:[
		// 			"@babel/plugin-syntax-dynamic-import",
		// 			"@babel/transform-runtime",
		// 			"@babel/plugin-proposal-class-properties"
		// 		]
		// 	}
		// },	
		]
	},

	plugins: [
		new ExtractTextPlugin('styles.css')
	]

}




module.exports = config;