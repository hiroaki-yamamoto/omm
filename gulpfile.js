const gulp = require("gulp");
const q = require("q");
const rimraf = require("rimraf");

gulp.task("clean", gulp.series(
  () => q.nfcall(rimraf, "?(tests|omm)/**/?(*.pyc|__pycache__)"),
));
