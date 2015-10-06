'use strict';

module.exports = function (config) {
    var configuration = {

        'plugins': [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-phantomjs-launcher',
            'karma-jasmine',
            'karma-mocha-reporter',
            'karma-coverage',
            'karma-ng-html2js-preprocessor'
        ],

        'frameworks': ['jasmine'],

        'basePath': '../',

        'files': [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/lodash/lodash.js',
            'bower_components/sprintf/src/sprintf.js',
            'bower_components/angular/angular.js',
            'bower_components/angular-route/angular-route.js',
            'bower_components/angular-route/angular-route.js',
            'bower_components/angular-animate/angular-animate.js',
            'bower_components/angular-sanitize/angular-sanitize.js',
            'bower_components/restangular/dist/restangular.js',
            'bower_components/angular-strap/dist/angular-strap.js',
            'bower_components/angular-strap/dist/angular-strap.tpl.js',
            'bower_components/angular-gettext/dist/angular-gettext.js',
            'bower_components/angular-smart-table/dist/smart-table.js',

            'bower_components/angular-mocks/angular-mocks.js',
            'bower_components/jasmine-promise-matchers/dist/jasmine-promise-matchers.js',

            'app/js/**/*.js',
            'app/partials/**/*.html',

            'test/unit/**/*.js',
            'test/functional/**/*.js'
        ],

        'exclude': [],

        'autoWatch': true,

        'browsers': ['PhantomJS'],

        'captureTimeout': 30000,

        'browserNoActivityTimeout': 60000,

        'customLaunchers': {
            'Chrome_travis_ci': {
                'base': 'Chrome',
                'flags': ['--no-sandbox']
            }
        },

        'colors': true,

        'logLevel': config.LOG_INFO,

        'reportSlowerThan': 200,

        'preprocessors': {
            'app/js/**/*.js': ['coverage'],
            'app/partials/**/*.html': ['ng-html2js']
        },

        'ngHtml2JsPreprocessor': {
            'stripPrefix': 'app/',
            'moduleName': 'partials'
        },

        'reporters': ['mocha', 'coverage'],

        'mochaReporter': {
            'ignoreSkipped': true
        },

        'coverageReporter': {
            'reporters': [
                {'type': 'lcovonly', 'dir': 'tmp/coverage/'},
                {'type': 'text-summary'},
                {'type': 'text'}
            ]
        }

    };

    if (process.env.TRAVIS) {
        configuration.browsers = ['Chrome_travis_ci'];
    }

    config.set(configuration);
};
