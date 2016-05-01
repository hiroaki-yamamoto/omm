gulp = require "gulp"
toolbox = require "hyamamoto-job-toolbox"

toolbox.python "", "omm", [
  "--with-coverage",
  "--cover-erase",
  "--cover-package=app",
  "--all"
]

gulp.task "test", ["python.tox"], ->
  # combine coverage
  toolbox.virtualenv(
    "coverage combine python27.coverage python35.coverage"
  ).then(
    -> toolbox.virtualenv("coverage report -m")
  )
gulp.task "default", ->
  gulp.watch(["omm/**/*.py", "tests/**/*.py"], ["test"])
