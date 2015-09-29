'use strict';

module.exports = function (grunt) {
    var production = grunt.option('p') || grunt.option('production');

    grunt.initConfig({
        'banner': '<%= grunt.package.name %> v<%= grunt.package.version %> | ' + '<%= grunt.package.author %> | <%= grunt.package.license %> Licensed | ' +
                  '<%= grunt.template.today("yyyy-mm-dd HH:MM:ss") %>',
        'min': production ? '.min' : '',

        'clean': {
            'dist': ['app/dist']
        },

        'copy': {
            'res_font_awesome': {
                'expand': true,
                'nonull': true,
                'cwd': 'bower_components/font-awesome/fonts/',
                'src': ['**'],
                'dest': 'app/dist/fonts/'
            },
            'res_bootstrap': {
                'expand': true,
                'nonull': true,
                'cwd': 'bower_components/bootstrap/dist/fonts/',
                'src': ['**'],
                'dest': 'app/dist/fonts/'
            },
            'res_flag_icon_css': {
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
                'banner': '/*! <%= banner %> */\n',
                'sourceMap': production
            },
            'res_js': {
                'src': [
                    'bower_components/jquery/dist/jquery<%= min %>.js',
                    'bower_components/lodash/lodash<%= min %>.js',
                    'bower_components/angular/angular<%= min %>.js',

                    'bower_components/angular-route/angular-route<%= min %>.js',
                    //'bower_components/angular-animate/angular-animate<%= min %>.js',
                    'bower_components/angular-sanitize/angular-sanitize<%= min %>.js',
                    'bower_components/restangular/dist/restangular<%= min %>.js',
                    'bower_components/angular-strap/dist/angular-strap<%= min %>.js',
                    'bower_components/angular-strap/dist/angular-strap.tpl<%= min %>.js',
                    'bower_components/angular-gettext/dist/angular-gettext<%= min %>.js',
                    'bower_components/angular-smart-table/dist/smart-table<%= min %>.js'
                ],
                'dest': 'app/dist/js/resources<%= min %>.js'
            },
            'app_js': {
                'src': ['app/js/**/*.js'],
                'dest': 'app/dist/js/storekeeper.js'
            },
            'res_css': {
                'src': [
                    'bower_components/bootstrap/dist/css/bootstrap<%= min %>.css',
                    'bower_components/bootstrap-additions/dist/bootstrap-additions<%= min %>.css',
                    'bower_components/angular-motion/dist/angular-motion<%= min %>.css',
                    'bower_components/font-awesome/css/font-awesome<%= min %>.css',
                    'bower_components/flag-icon-css/css/flag-icon<%= min %>.css'
                ],
                'dest': 'app/dist/css/resources<%= min %>.css',
                'options': {
                    'sourceMap': false  // FIXME: Workaround for "Warning: Cannot call method 'substr' of undefined"
                }
            },
            'app_css': {
                'src': ['app/css/**/*.css'],
                'dest': 'app/dist/css/storekeeper.css'
            }
        },

        'uglify': {
            'options': {
                'banner': '/*! <%= banner %> */\n',
                'sourceMap': production,
                'sourceMapIncludeSources': true,
                'sourceMapIn': '<%= concat.app_js.dest %>.map'
            },
            'app_js': {
                'files': {
                    'app/dist/js/storekeeper.min.js': ['<%= concat.app_js.dest %>']
                }
            }
        },

        'cssmin': {
            'options': {
                'banner': '/*! <%= banner %> */\n',
                'sourceMap': production
            },
            'app_css': {
                'files': {
                    'app/dist/css/storekeeper.min.css': ['<%= concat.app_css.dest %>']
                }
            }
        },

        'replace': {
            'index_html': {
                'src': 'app/index.html',
                'dest': 'app/index.html',
                'replacements': [{
                    'from': /(|\.min)\.(css|js)[^"]*"/g,
                    'to': '.$2"'
                }]
            },
            'index_html_min': {
                'src': 'app/index.html',
                'dest': 'app/index.html',
                'replacements': [{
                    'from': /(|\.min)\.(css|js)[^"]*"/g,
                    'to': '.min.$2?v=<%= grunt.package.version %>"'
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
                'tasks': ['app_css']
            },
            'js': {
                'files': [
                    'app/js/**/*.js',
                    'app/partials/**/*.html',
                    'po/*.po'
                ],
                'tasks': ['nggettext_extract', 'app_js']
            },
            'html': {
                'files': [
                    'app/partials/**/*.html'
                ],
                'tasks': ['nggettext_extract']
            },
            'index_html': {
                'files': [
                    'app/index.html'
                ],
                'tasks': ['nggettext_extract', 'app_index_html']
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

    grunt.registerTask('app_res', 'Prepare external resources', [
        'copy'
    ]);

    grunt.registerTask('app_css', 'Prepare CSS files', function () {
        grunt.task.run('concat:res_css');
        grunt.task.run('concat:app_css');
        if (production) {
            grunt.task.run('cssmin');
        }
    });

    grunt.registerTask('app_js', 'Prepare JS files', function () {
        grunt.task.run('nggettext_compile');
        grunt.task.run('ngtemplates');
        grunt.task.run('concat:res_js');
        grunt.task.run('concat:app_js');
        if (production) {
            grunt.task.run('uglify');
        }
    });

    grunt.registerTask('app_index_html', 'Prepare HTML files', function () {
        if (production) {
            grunt.task.run('replace:index_html_min');
        } else {
            grunt.task.run('replace:index_html');
        }
    });

    grunt.registerTask('prepare', 'Prepare environment (you can use [-p, --production])', [
        'clean',
        'app_res',
        'app_css',
        'app_js',
        'app_index_html'
    ]);

    grunt.registerTask('auto_prepare', 'Prepare environment (you can use [-p, --production]) and following up changes', [
        'prepare',
        'watch'
    ]);

    grunt.registerTask('default', [
        'prepare'
    ]);
};
