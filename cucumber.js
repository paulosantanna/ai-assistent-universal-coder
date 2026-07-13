module.exports = {
  default: {
    paths: ["features/js/**/*.feature"],
    require: ["features/js/step_definitions/**/*.cjs"],
    format: ["progress"],
  },
};
