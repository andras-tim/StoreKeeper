module.exports = function(config) {
    config.set({

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

            'app/bower_components/angular-mocks/angular-mocks.js',

            'app/js/**/*.js',
            'test/unit/**/*.js'
        ],

        autoWatch: true,

        frameworks: ['jasmine'],

        browsers: ['Chrome'],

        plugins: [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine'
        ],

        junitReporter: {
            outputFile: 'test_out/unit.xml',
            suite: 'unit'
        }

    });
};
