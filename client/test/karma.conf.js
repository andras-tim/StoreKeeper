'use strict';

module.exports = function(config) {
    var configuration = {

        plugins: [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine',
            'karma-coverage'
        ],

        frameworks: ['jasmine'],

        basePath: '../',

        files: [
            'app/bower_components/jquery/dist/jquery.js',
            'app/bower_components/lodash/dist/lodash.js',
            'app/bower_components/angular/angular.js',
            'app/bower_components/angular-route/angular-route.js',
            'app/bower_components/angular-route/angular-route.js',
            'app/bower_components/angular-animate/angular-animate.js',
            'app/bower_components/angular-sanitize/angular-sanitize.js',
            'app/bower_components/restangular/dist/restangular.js',
            'app/bower_components/angular-strap/dist/angular-strap.js',
            'app/bower_components/angular-strap/dist/angular-strap.tpl.js',
            'app/bower_components/angular-gettext/dist/angular-gettext.js',
            'app/bower_components/angular-smart-table/dist/smart-table.js',

            'app/bower_components/angular-mocks/angular-mocks.js',

            'app/js/dist/storekeeper.js',
            'test/unit/**/*.js'
        ],

        exclude: [],

        autoWatch: true,

        browsers: ['Chrome'],

        customLaunchers: {
            Chrome_travis_ci: {
                base: 'Chrome',
                flags: ['--no-sandbox']
            }
        },

        colors: true,

        logLevel: config.LOG_INFO,

        reportSlowerThan: 500,

        preprocessors: {
            'app/js/storekeeper.js': 'coverage'
        },

        reporters: ['progress', 'dots', 'coverage'],

        coverageReporter: {
            reporters: [
                {type: 'lcovonly', dir: 'tmp/coverage/'},
                {type: 'text-summary'},
                {type: 'text'}
            ]
        }

    };

    if (process.env.TRAVIS) {
        configuration.browsers = ['Chrome_travis_ci'];
    }

    config.set(configuration);
};
