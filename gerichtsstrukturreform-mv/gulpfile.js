var gulp = require('gulp'),
  connect = require('gulp-connect'),
  minifyCss = require('gulp-minify-css'),
  concat = require('gulp-concat'),
  uglifiy = require('gulp-uglify');
;
 
gulp.task('connect', function() {
  connect.server({
    livereload: true
  });
});
 
gulp.task('html', function () {
  gulp.src('.html')
    .pipe(connect.reload());
});
 
gulp.task('watch', function () {
  gulp.watch(['.html'], ['html']);
});


gulp.task('css', function () {
  gulp.src(['bower_components/bootstrap/dist/css/bootstrap.min.css', 'style.css'])
    .pipe(concat('all.min.css'))
    .pipe(minifyCss())
    .pipe(gulp.dest('.'));
});
 
gulp.task('js', function () {
  gulp.src(['bower_components/jquery/dist/jquery.min.js','bower_components/bootstrap/dist/js/bootstrap.min.js', 'bower_components/cartodb.js/cartodb.js', 'bower_components/d3/d3.min.js', 'app.js'])
    .pipe(concat('all.min.js'))
    .pipe(uglifiy())
    .pipe(gulp.dest('.'));
});
 
gulp.task('default', ['connect', 'watch']);
