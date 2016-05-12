gulp = require "gulp"
q = require "q"
rimraf = require "rimraf"
toolbox = require "hyamamoto-job-toolbox"

toolbox.python "", "omm", [
  "--with-coverage",
  "--cover-erase",
  "--cover-package=omm",
  "--all"
]

gulp.task "test", ["python.tox"], ->
  # combine coverage
  toolbox.virtualenv(
    "coverage combine python27.coverage python35.coverage"
  ).then(
    -> toolbox.virtualenv("coverage report -m")
  )
gulp.task "clean", ->
  q.nfcall(rimraf, "?(tests|omm)/**/?(*.pyc|__pycache__)")
gulp.task "default", ->
  gulp.watch(["omm/**/*.py", "tests/**/*.py"], ["test"])
