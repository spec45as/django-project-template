var webpack = require("webpack");
var BowerWebpackPlugin = require("bower-webpack-plugin");


module.exports = {
    context: __dirname,
    devtool: "#inline-source-map",
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: [/node_modules/, /vendor/],
                loader: "babel-loader",
                query: {
                    optional: ["es7.classProperties"],
                    comments: false
                }
            }
        ],
        noParse: [
            new RegExp('.*vendor.*')
        ]
    },
    plugins: [new BowerWebpackPlugin({
        modulesDirectories: ["{{ project_name }}/{{ project_name }}/static/vendor"],
    })]
};
