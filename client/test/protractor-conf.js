'use strict';

exports.config = {
    allScriptsTimeout: 11000,

    specs: [
        'e2e/*.js'
    ],

    capabilities: {
        'browserName': 'chrome',
        'chromeOptions': {
            args: []
        }
    },

    chromeOnly: true,

    baseUrl: 'http://localhost:8000/',

    framework: 'jasmine',

    jasmineNodeOpts: {
        defaultTimeoutInterval: 30000
    }
};

if (process.env.TRAVIS) {
    exports.config.capabilities.chromeOptions.args = ['--no-sandbox'];
}
