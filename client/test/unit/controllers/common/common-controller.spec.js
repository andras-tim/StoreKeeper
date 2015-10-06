'use strict';

describe('Controllers/Common: CommonController', function () {
    var test;

    beforeEach(module('appControllers.common'));

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
                '$rootScope': {
                    '$on': function (name, func) {
                        test.eventListeners[name] = func;
                    }
                },
                '$scope': {},
                '$location': {},
                '$route': {
                    'current': {}
                },
                '$aside': {},
                '$event': {
                    'preventDefault': function () {}
                },
                '$modal': {
                    '$promise': {
                        'then': function (func) {
                            return func();
                        }
                    },
                    'hide': function () {}
                },
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
                },
                'ShortcutFactory': function () {}
            },

            dependencies = {
                '$scope': mocks.$scope,
                '$rootScope': mocks.$rootScope,
                '$location': mocks.$location,
                '$route': mocks.$route,
                '$aside': mocks.$aside,
                'ConfigFactory': mocks.ConfigFactory,
                'PageFactory': mocks.PageFactory,
                'SessionFactory': mocks.SessionFactory,
                'CommonFactory': mocks.CommonFactory,
                'ShortcutFactory': mocks.ShortcutFactory
            },

            injectController = function () {
                spyOn(mocks.$event, 'preventDefault').and.stub();
                spyOn(mocks.$modal, 'hide').and.stub();
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
        test.eventListeners = {};
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

    //describe('modal handling', function () {
    //    beforeEach(function () {
    //        test.injectController();
    //    });
    //
    //    it('can open new modal', function () {
    //        test.eventListeners['modal.show'](test.mocks.$event, test.mocks.$modal, null);
    //        expect(test.mocks.$event.preventDefault).not.toHaveBeenCalled();
    //        expect(test.mocks.$modal.hide).not.toHaveBeenCalled();
    //    });
    //
    //    it('can change url when has not opened any modal', function () {
    //        test.eventListeners.$routeChangeSuccess(test.mocks.$event, null, null);
    //        expect(test.mocks.$event.preventDefault).not.toHaveBeenCalled();
    //    });
    //
    //    it('close the one opened modal when change url', function () {
    //        test.eventListeners['modal.show'](test.mocks.$event, test.mocks.$modal, null);
    //        test.eventListeners.$routeChangeSuccess(test.mocks.$event, null, null);
    //        expect(test.mocks.$event.preventDefault).not.toHaveBeenCalled();
    //        expect(test.mocks.$modal.hide).toHaveBeenCalled();
    //    });
    //});
});
