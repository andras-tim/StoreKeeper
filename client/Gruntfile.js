module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-angular-gettext');

  grunt.initConfig({
    nggettext_extract: {
      pot: {
        files: {
          'po/template.pot': [
            'app/*.html',
            'app/js/*.js',
            'app/partials/*.html'
          ]
        }
      }
    },
    nggettext_compile: {
      all: {
        files: {
          'app/js/translations.js': ['po/*.po']
        }
      }
    }
  });
};
