'use strict';

describe('CommonController', function () {
    var test;

    beforeEach(module('appControllers'));

    beforeEach(function () {
        test = this;

        var data = {
                'config': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': null
                },
                'configWithForcedLanguage': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': 'hu'
                }
            },

            mocks = {
                '$scope': {},
                'ConfigFactory': {
                    'getConfig': function () {
                        return helper.promiseMock(test, 'configResolved', test.config, test.config);
                    }
                },
                'PageFactory': {
                    'getWindowTitle': function () {
                        return 'Foo';
                    }
                },
                'SessionFactory': {
                    'isAuthenticated': function () {
                        return true;
                    }
                },
                'CommonFactory': {
                    'showResponseError': function () {}
                }
            },

            dependencies = {
                '$scope': mocks.$scope,
                'ConfigFactory': mocks.ConfigFactory,
                'PageFactory': mocks.PageFactory,
                'SessionFactory': mocks.SessionFactory,
                'CommonFactory': mocks.CommonFactory
            },

            injectController = function () {
                spyOn(mocks.CommonFactory, 'showResponseError').and.stub();
                spyOn(mocks.SessionFactory, 'isAuthenticated').and.callThrough();
                spyOn(mocks.PageFactory, 'getWindowTitle').and.callThrough();

                inject(function ($controller, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$q = $q;

                    dependencies.$scope = mocks.$scope;

                    $controller('CommonController', dependencies);
                });

                test.$rootScope.$apply();
            };

        this.data = data;
        this.mocks = mocks;
        this.injectController = injectController;
    });

    beforeEach(function () {
        test.config = test.data.config;
        test.configResolved = true;
    });

    describe('config', function () {
        it('drop error when can not load config', function () {
            test.configResolved = false;
            test.injectController();

            expect(test.mocks.CommonFactory.showResponseError).toHaveBeenCalledWith(test.data.config);
        });
    });

    describe('authentication', function () {
        it('isAuthenticated() is same as isAuthenticated() of SessionFactory', function () {
            test.injectController();

            expect(test.mocks.SessionFactory.isAuthenticated).not.toHaveBeenCalled();
            expect(test.mocks.$scope.isAuthenticated()).toBeTruthy();
            expect(test.mocks.SessionFactory.isAuthenticated).toHaveBeenCalled();
        });
    });

    describe('titles', function () {
        beforeEach(function () {
            test.injectController();
        });

        it('check appTitle', function () {
            expect(test.mocks.$scope.appTitle).toBe(test.data.config.app_title);
        });

        it('check getWindowTitle()', function () {
            expect(test.mocks.PageFactory.getWindowTitle).not.toHaveBeenCalled();
            expect(test.mocks.$scope.getWindowTitle()).toBe('Foo');
            expect(test.mocks.PageFactory.getWindowTitle).toHaveBeenCalled();
        });
    });
});
