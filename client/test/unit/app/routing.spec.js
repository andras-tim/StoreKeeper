'use strict';

describe('App: routing', function () {
    var test,
        pages,
        mainPage,
        loginPage;

    beforeEach(module('storekeeperApp'));

    beforeEach(function () {
        test = this;

        var data = {
                'config': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': 'hu'
                },
                'session': {
                    'id': 2,
                    'username': 'foo',
                    'email': 'foo@localhost',
                    'admin': false,
                    'disabled': false
                }
            },

            mocks = {
                'ConfigFactory': {
                    'getConfig': function () {
                        return {
                            'then': function (onResolved) {
                                onResolved(data.config);
                            }
                        };
                    }
                },
                'SessionFactory': {
                    'getSession': function () {
                        return {
                            'then': function (onResolved, onRejected) {
                                if (test.hasSession) {
                                    onResolved(data.session);
                                } else {
                                    onRejected();
                                }
                            }
                        };
                    }
                }
            },

            injectApp = function () {
                module(function ($provide) {
                    $provide.value('ConfigFactory', mocks.ConfigFactory);
                    $provide.value('SessionFactory', mocks.SessionFactory);
                });

                // inject() calls run() and config() directives
                inject(function ($rootScope, $route, $location, $httpBackend) {
                    test.$rootScope = $rootScope;
                    test.$route = $route;
                    test.$location = $location;
                    test.$httpBackend = $httpBackend;
                });
            },

            mockUrl = function (mockedUrl, response) {
                if (!response) {
                    response = '';
                }
                test.requestHandler = test.$httpBackend.when('GET', mockedUrl).respond(200, response);
                test.$httpBackend.expectGET(mockedUrl);
            };

        this.data = data;
        this.mocks = mocks;
        this.injectApp = injectApp;
        this.mockUrl = mockUrl;
    });

    pages = [
        {
            'entryPoint': '/login',
            'templateUrl': 'partials/views/login.html',
            'controller': 'LoginController',
            'sessionRequired': false
        },
        {
            'entryPoint': '/items',
            'templateUrl': 'partials/views/items.html',
            'controller': 'ItemsController',
            'sessionRequired': true
        }
    ];
    loginPage = pages[0];
    mainPage = pages[1];

    afterEach(function () {
        test.$httpBackend.flush();
        test.$httpBackend.verifyNoOutstandingExpectation();
        test.$httpBackend.verifyNoOutstandingRequest();
    });

    describe('without session', function () {

        beforeEach(function () {
            test.hasSession = false;
        });

        it('redirect / URL to login page', function () {
            test.injectApp();
            test.mockUrl(mainPage.templateUrl);
            test.mockUrl(loginPage.templateUrl);

            expect(test.$route.current).toBeUndefined();

            test.$location.path('/');
            test.$rootScope.$apply();

            expect(test.$route.current.loadedTemplateUrl).toBe(loginPage.templateUrl);
            expect(test.$route.current.controller).toBe(loginPage.controller);
        });

        /*jshint -W083 */ //Disable warning for function created inside loop
        pages.forEach(function (data) {

            if (data.sessionRequired) {
                it('redirect ' + data.entryPoint + ' URL to login page', function () {
                    test.injectApp();
                    test.mockUrl(data.templateUrl);
                    test.mockUrl(loginPage.templateUrl);

                    expect(test.$route.current).toBeUndefined();

                    test.$location.path(mainPage.entryPoint);
                    test.$rootScope.$apply();

                    expect(test.$route.current.loadedTemplateUrl).toBe(loginPage.templateUrl);
                    expect(test.$route.current.controller).toBe(loginPage.controller);
                });
                return;
            }

            it('load ' + data.entryPoint + ' URL', function () {
                test.injectApp();
                test.mockUrl(data.templateUrl);

                expect(test.$route.current).toBeUndefined();

                test.$location.path(data.entryPoint);
                test.$rootScope.$apply();

                expect(test.$route.current.loadedTemplateUrl).toBe(data.templateUrl);
                expect(test.$route.current.controller).toBe(data.controller);
            });
        });
    });

    describe('with session', function () {

        beforeEach(function () {
            test.hasSession = true;
        });

        it('redirect / URL to main page', function () {
            test.injectApp();
            test.mockUrl(mainPage.templateUrl);

            expect(test.$route.current).toBeUndefined();

            test.$location.path('/');
            test.$rootScope.$apply();

            expect(test.$route.current.loadedTemplateUrl).toBe(mainPage.templateUrl);
            expect(test.$route.current.controller).toBe(mainPage.controller);
        });

        /*jshint -W083 */ //Disable warning for function created inside loop
        pages.forEach(function (data) {
            it('load ' + data.entryPoint + ' URL', function () {
                test.injectApp();
                test.mockUrl(data.templateUrl);

                expect(test.$route.current).toBeUndefined();

                test.$location.path(data.entryPoint);
                test.$rootScope.$apply();

                expect(test.$route.current.loadedTemplateUrl).toBe(data.templateUrl);
                expect(test.$route.current.controller).toBe(data.controller);
            });
        });
    });
});
