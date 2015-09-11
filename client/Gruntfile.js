'use strict';

module.exports = function (grunt) {
    var production = grunt.option('p') || grunt.option('production');

    grunt.initConfig({
        'pkg': grunt.file.readJSON('package.json'),
        'banner': '<%= pkg.name %> v<%= pkg.version %> | ' + '<%= pkg.author %> | <%= pkg.license %> Licensed | ' +
                  '<%= grunt.template.today("yyyy-mm-dd HH:MM:ss") %>',

        'clean': {
            'dist': ['app/dist']
        },

        'copy': {
            'res-font-awesome': {
                'expand': true,
                'nonull': true,
                'cwd': 'bower_components/font-awesome/fonts/',
                'src': ['**'],
                'dest': 'app/dist/fonts/'
            },
            'res-bootstrap': {
                'expand': true,
                'nonull': true,
                'cwd': 'bower_components/bootstrap/dist/fonts/',
                'src': ['**'],
                'dest': 'app/dist/fonts/'
            },
            'res-flag-icon-css': {
                'expand': true,
                'nonull': true,
                'cwd': 'bower_components/flag-icon-css/flags/4x3/',
                'src': ['**'],
                'dest': 'app/dist/flags/4x3'
            }
        },

        'nggettext_extract': {
            'pot': {
                'files': {
                    'po/template.pot': [
                        'app/*.html',
                        'app/js/**/*.js',
                        'app/partials/**/*.html'
                    ]
                }
            }
        },
        'nggettext_compile': {
            'po': {
                'files': {
                    'app/js/translations.tmp.js': ['po/*.po']
                }
            }
        },

        'ngtemplates': {
            'partials': {
                'options': {
                    'module': 'storekeeperApp',
                    'htmlmin': {
                        'collapseBooleanAttributes': true,
                        'collapseWhitespace': true,
                        //'removeAttributeQuotes': true,
                        'removeComments': true,
                        'removeEmptyAttributes': true,
                        'removeRedundantAttributes': true,
                        'removeScriptTypeAttributes': true,
                        'removeStyleLinkTypeAttributes': true
                    }
                },
                'cwd': 'app',
                'src': ['partials/**/*.html'],
                'dest': 'app/js/partials.tmp.js'
            }
        },

        'concat': {
            'options': {
                'sourceMap': production
            },
            'js': {
                'src': [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/lodash/lodash.js',
                    'bower_components/angular/angular.js',

                    'bower_components/angular-route/angular-route.js',
                    //'bower_components/angular-animate/angular-animate.js',
                    'bower_components/angular-sanitize/angular-sanitize.js',
                    'bower_components/restangular/dist/restangular.js',
                    'bower_components/angular-strap/dist/angular-strap.js',
                    'bower_components/angular-strap/dist/angular-strap.tpl.js',
                    'bower_components/angular-gettext/dist/angular-gettext.js',
                    'bower_components/angular-smart-table/dist/smart-table.js',

                    'app/js/**/*.js'
                ],
                'dest': 'app/dist/js/storekeeper.js'
            },
            'css': {
                'src': [
                    'bower_components/bootstrap/dist/css/bootstrap.css',
                    'bower_components/bootstrap-additions/dist/bootstrap-additions.css',
                    'bower_components/angular-motion/dist/angular-motion.css',
                    'bower_components/font-awesome/css/font-awesome.css',
                    'bower_components/flag-icon-css/css/flag-icon.css',

                    'app/css/**/*.css'
                ],
                'dest': 'app/dist/css/storekeeper.css'
            }
        },

        'uglify': {
            'options': {
                'banner': '/*! <%= banner %> */\n',
                'sourceMap': production,
                'sourceMapIncludeSources': true,
                'sourceMapIn': '<%= concat.js.dest %>.map'
            },
            'js': {
                'files': {
                    'app/dist/js/storekeeper.min.js': ['<%= concat.js.dest %>']
                }
            }
        },

        'cssmin': {
            'options': {
                'banner': '/*! <%= banner %> */\n',
                'sourceMap': production
            },
            'css': {
                'files': {
                    'app/dist/css/storekeeper.min.css': ['<%= concat.css.dest %>']
                }
            }
        },

        'replace': {
            'html': {
                'src': 'app/index.html',
                'dest': 'app/index.html',
                'replacements': [{
                    'from': /(|\.min)\.(css|js)[^"]*"/g,
                    'to': '.$2"'
                }]
            },
            'html-min': {
                'src': 'app/index.html',
                'dest': 'app/index.html',
                'replacements': [{
                    'from': /(|\.min)\.(css|js)[^"]*"/g,
                    'to': '.min.$2?v=<%= pkg.version %>"'
                }]
            }
        },

        'watch': {
            'options': {
                'spawn': false,
                'dateFormat': function (time) {
                    grunt.log.writeln('\n>> finished in ' + time + 'ms at ' + (new Date()).toString() + '\n\n');
                    grunt.log.writeln('Waiting for more changes...');
                }
            },
            'css': {
                'files': [
                    'app/css/**/*.css'
                ],
                'tasks': ['app-css']
            },
            'js': {
                'files': [
                    'app/js/**/*.js',
                    'app/partials/**/*.html',
                    'po/*.po'
                ],
                'tasks': ['app-js']
            },
            'html': {
                'files': [
                    'app/index.html'
                ],
                'tasks': ['app-html']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-angular-gettext');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-text-replace');

    grunt.registerTask('app-res', 'Prepare external resources', [
        'copy'
    ]);
    grunt.registerTask('app-css', 'Prepare CSS files', function () {
        grunt.task.run('concat:css');
        if (production) {
            grunt.task.run('cssmin');
        }
    });
    grunt.registerTask('app-js', 'Prepare JS files', function () {
        grunt.task.run('nggettext_compile');
        grunt.task.run('ngtemplates');
        grunt.task.run('concat:js');
        if (production) {
            grunt.task.run('uglify');
        }
    });
    grunt.registerTask('app-html', 'Prepare HTML files', function () {
        if (production) {
            grunt.task.run('replace:html-min');
        } else {
            grunt.task.run('replace:html');
        }
    });
    grunt.registerTask('prepare', 'Prepare environment (you can use [-p, --production])', [
        'clean',
        'app-res',
        'app-css',
        'app-js',
        'app-html'
    ]);
    grunt.registerTask('default', [
        'prepare'
    ]);
};
