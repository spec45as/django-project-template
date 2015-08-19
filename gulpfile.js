'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');


gulp.task('sass', function () {
  var options = {
        includePaths: ['./proj/proj/static'],
        outputStyle: 'compressed'
  };

  gulp.src('./proj/**/static/assets/styles/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass(options).on('error', sass.logError))
    .pipe(rename('build.css'))
    .pipe(autoprefixer({
      browsers: ['last 10 versions'],
      cascade: false
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./proj/proj/static/build/'));
});
