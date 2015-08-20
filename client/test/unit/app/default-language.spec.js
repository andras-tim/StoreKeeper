'use strict';

describe('App: default language', function () {
    var test;

    beforeEach(module('storekeeperApp'));

    beforeEach(function () {
        test = this;

        var data = {
                'configWithoutForcedLanguage': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': null
                },
                'configWithForcedLanguage': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': 'orange'
                }
            },

            mocks = {
                '$window': {
                    'document': {},
                    'navigator': {
                        'language': '',
                        'userLanguage': ''
                    }
                },
                'ConfigFactory': {
                    'getConfig': function () {
                        return {
                            'then': function (onResolved) {
                                onResolved(test.config);
                            }
                        };
                    }
                },
                'SessionFactory': {
                    'getSession': function () {
                        return {
                            'then': function (onResolved, onRejected) {
                                onRejected();
                            }
                        };
                    }
                },
                'gettextCatalog': {
                    'baseLanguage': null,
                    'debug': null,
                    'setCurrentLanguage': function () {},
                    'setStrings': function () {}
                }
            },

            injectApp = function () {
                module(function ($provide) {
                    $provide.value('$window', mocks.$window);
                    $provide.value('ConfigFactory', mocks.ConfigFactory);
                    $provide.value('SessionFactory', mocks.SessionFactory);
                    $provide.value('gettextCatalog', mocks.gettextCatalog);
                });
                spyOn(mocks.gettextCatalog, 'setCurrentLanguage').and.stub();

                // inject() calls run() and config() directives
                inject();
            };

        this.data = data;
        this.mocks = mocks;
        this.injectApp = injectApp;
    });

    describe('without forced language', function () {

        beforeEach(function () {
            test.config = test.data.configWithoutForcedLanguage;
        });

        it('base language is have to be english', function () {
            test.injectApp();

            expect(test.mocks.gettextCatalog.baseLanguage).toEqual('en');
        });

        it('set to apple when language is apple in browser', function () {
            test.mocks.$window.navigator.language = 'apple';
            test.injectApp();

            expect(test.mocks.gettextCatalog.setCurrentLanguage).toHaveBeenCalledWith('apple');
        });

        it('set to apple when language is apple-PEACH in browser', function () {
            test.mocks.$window.navigator.language = 'apple-PEACH';
            test.injectApp();

            expect(test.mocks.gettextCatalog.setCurrentLanguage).toHaveBeenCalledWith('apple');
        });

        it('set to apple when userLanguage is apple in browser', function () {
            test.mocks.$window.navigator.userLanguage = 'apple';
            test.injectApp();

            expect(test.mocks.gettextCatalog.setCurrentLanguage).toHaveBeenCalledWith('apple');
        });

        it('set to apple when userLanguage is apple-PEACH in browser', function () {
            test.mocks.$window.navigator.userLanguage = 'apple-PEACH';
            test.injectApp();

            expect(test.mocks.gettextCatalog.setCurrentLanguage).toHaveBeenCalledWith('apple');
        });

        it('userLanguage property has higher priority than language', function () {
            test.mocks.$window.navigator.language = 'apple';
            test.mocks.$window.navigator.userLanguage = 'peach';
            test.injectApp();

            expect(test.mocks.gettextCatalog.setCurrentLanguage).toHaveBeenCalledWith('peach');
        });
    });

    describe('with forced language', function () {

        beforeEach(function () {
            test.config = test.data.configWithForcedLanguage;
        });

        it('overrides the browser language', function () {
            test.mocks.$window.navigator.language = 'apple';
            test.mocks.$window.navigator.userLanguage = 'peach';
            test.injectApp();

            expect(test.mocks.gettextCatalog.setCurrentLanguage).toHaveBeenCalledWith('orange');
        });
    });
});
