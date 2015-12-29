'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');
var webpack = require("webpack");
var webpackStream = require("webpack-stream");
var BowerWebpackPlugin = require("bower-webpack-plugin");


var BASE_DIR = './src';
var PROJECT_DIR = BASE_DIR + '/dom';
var STATIC_DIR = PROJECT_DIR + '/static';
var VENDOR_DIR = STATIC_DIR + '/vendor';
var BUILD_DIR = STATIC_DIR + '/build/';
var JS_PATH = BASE_DIR + '/**/static/assets/**/*.js';
var CSS_PATH = BASE_DIR + '/**/static/assets/**/*.scss';
var BUNDLE_ENTRY = STATIC_DIR + '/assets/js/main.js';


var NODE_ENV = process.env.NODE_ENV || 'development';


if (NODE_ENV == 'development') {
    console.log('>>> Development mode\n');
    var webpackPlugins = [
        new BowerWebpackPlugin({modulesDirectories: [VENDOR_DIR]}),
        new webpack.optimize.CommonsChunkPlugin("vendor", "vendor.bundle.js")
    ]
} else {
    console.log('>>> Production mode\n');
    var webpackPlugins = [
        new BowerWebpackPlugin({modulesDirectories: [VENDOR_DIR]}),
        new webpack.optimize.UglifyJsPlugin(),
        new webpack.optimize.CommonsChunkPlugin("vendor", "vendor.bundle.js")
    ]
}


var webpackConfig = {
    context: __dirname,
    entry: {
        bundle: BUNDLE_ENTRY,
        vendor: ['react']
    },
    output: {
        filename: '[name].js',
        library: '[name]'
    },
    devtool: 'source-map',
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
    plugins: webpackPlugins
};


gulp.task('sass', function () {
  var options = {
        includePaths: [STATIC_DIR],
        outputStyle: 'compressed'
  };

  gulp.src(CSS_PATH)
    .pipe(sourcemaps.init())
    .pipe(sass(options).on('error', sass.logError))
    .pipe(rename('bundle.css'))
    .pipe(autoprefixer({
      browsers: ['last 10 versions'],
      cascade: false
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(BUILD_DIR));
});


gulp.task('js', function () {
  return gulp.src(BUNDLE_ENTRY)
    .pipe(webpackStream(webpackConfig))
    .pipe(gulp.dest(BUILD_DIR));
});


gulp.task('watch', function() {
  gulp.watch(CSS_PATH, ['sass']);
  gulp.watch(JS_PATH, ['js']);
});


if (NODE_ENV == 'development') {
    gulp.task('default', ['watch', 'sass', 'js']);
} else {
    gulp.task('default', ['sass', 'js']);
}
