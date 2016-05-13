"use strict";

let gulp = require('gulp');
let uglify = require('gulp-uglify');
let notify = require('gulp-notify');
let plumber = require('gulp-plumber');
let cssmin = require('gulp-cssmin');
let rename = require("gulp-rename");
let sass = require('gulp-sass');
let postcss = require('gulp-postcss');
let autoprefixer = require('autoprefixer');
let path = require('path');
let browserSync = require('browser-sync').create();
let webpack_stream = require('webpack-stream');
let webpackConfig = require('./webpack.config.js');

let spawn = require('child_process').spawn;
let argv = require('yargs')
    .default('host', '127.0.0.1')
    .default('port', 3000)
    .default('bsync-port', 8000)
    .argv;

let djangoAddress = argv.host + ":" + argv.port;
let config = {
    sass: {
        src: './assets/sass/index.scss',
        watch: './assets/sass/**/*.scss',
        dest: './src/{{ project_name }}/static/build/',
        destFileName: 'bundle.css',
        sassOptions: {
            includePaths: ['node_modules']
        }
    },
    js: {
        src: './assets/js/index.js',
        entry: {
            'bundle': './assets/js/index.js'
        },
        watch: './assets/js/**/*.jsx?',
        dest: './src/{{ project_name }}/static/build/'
    }
};


gulp.task('js:dev', function () {
    let cfg = Object.assign({}, webpackConfig.development, {entry: config.js.entry});

    return gulp.src(config.js.src)
        .pipe(webpack_stream(cfg))
        .on('error', function (error) {
            console.log(error.message);
            this.emit('end');
        })
        .pipe(gulp.dest(config.js.dest))
});


gulp.task('js:prod', function () {
    let cfg = Object.assign({}, webpackConfig.production, {entry: config.js.entry});
    return gulp.src(config.js.src)
        .pipe(webpack_stream(cfg))
        .pipe(gulp.dest(config.js.dest));
});


gulp.task('sass:dev', function () {
    return gulp.src(config.sass.src)
        .pipe(plumber())
        .pipe(sass(config.sass.sassOptions))
        .pipe(postcss([ autoprefixer({ browsers: ['last 10 versions'] }) ]))
        .pipe(rename(config.sass.destFileName))
        .pipe(gulp.dest(config.sass.dest))
        .pipe(browserSync.stream())
});


gulp.task('sass:prod', function () {
    return gulp.src(config.sass.src)
        .pipe(sass(config.sass.sassOptions))
        .pipe(postcss([ autoprefixer({ browsers: ['last 10 versions'] }) ]))
        .pipe(rename(config.sass.destFileName))
        .pipe(cssmin())
        .pipe(gulp.dest(config.sass.dest))
});


gulp.task('django-runserver', function () {
    if (!process.env['VIRTUAL_ENV']) {
        console.warn("WARNING: To run django you should activate virtual environment")
    } else {
        let args = ["src/manage.py", "runserver", djangoAddress];
        let python = process.env['VIRTUAL_ENV'] + '/bin/python';
        let runserver = spawn(python, args, {stdio: "inherit"});
        runserver.on('close', function (code) {
            if (code !== 0) {
                console.error('Django runserver exited with error code: ' + code);
            } else {
                console.log('Django runserver exited normally.');
            }
        });
    }
});


gulp.task('browsersync', ['django-runserver'], function () {
    browserSync.init({
        proxy: djangoAddress,
        port: argv['bsync-port']
    });
});


gulp.task('watch', function () {
    gulp.watch(config.sass.watch, ['sass:dev']);
});


// Run in development
gulp.task('default', ['sass:dev', 'js:dev', 'django-runserver', 'browsersync', 'watch']);


// Run before deploy to production
gulp.task('deploy', ['sass:prod', 'js:prod']);
