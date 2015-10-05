'use strict';

describe('Factories/Resource: SessionFactory', function () {
    var test;

    beforeEach(module('appFactories.resource'));

    beforeEach(function () {
        test = this;

        var afterInjects = [],

            data = {
                'unauthorizedResponse': {
                    'message': 'foo',
                    'status': 401
                },
                'unknownResponse': {
                    'message': 'bar',
                    'status': 404
                },
                'unauthorizedSession': {
                    'id': 0,
                    'username': null,
                    'email': null,
                    'admin': false,
                    'disabled': false
                },
                'authorizedByFooSession': {
                    'id': 2,
                    'username': 'foo',
                    'email': 'foo@localhost',
                    'admin': false,
                    'disabled': false
                },
                'authorizedByBarSession': {
                    'id': 3,
                    'username': 'bar',
                    'email': 'bar@localhost',
                    'admin': false,
                    'disabled': false
                }
            },

            mocks = {
                'Restangular': {
                    'stripRestangular': function (resp) {
                        return resp;
                    }
                },
                'SessionService': {
                    'one': function () {
                        return this;
                    },
                    'get': function () {
                        return this.promiseResults();
                    },
                    'post': function () {
                        return this.promiseResults();
                    },
                    'remove': function () {
                        return this.promiseResults();
                    },
                    'promiseResults': function () {
                        return helper.promiseMock(test, 'resultsResolved', test.results, test.results);
                    }
                },
                'CommonFactory': {
                    'showResponseError': function () {}
                }
            },

            injectFactory = function () {
                module(function ($provide) {
                    $provide.value('Restangular', mocks.Restangular);
                    $provide.value('SessionService', mocks.SessionService);
                    $provide.value('CommonFactory', mocks.CommonFactory);
                });
                spyOn(mocks.SessionService, 'get').and.callThrough();
                spyOn(mocks.SessionService, 'post').and.callThrough();
                spyOn(mocks.SessionService, 'remove').and.callThrough();
                spyOn(mocks.CommonFactory, 'showResponseError');

                installPromiseMatchers();

                inject(function ($injector, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$q = $q;

                    test.SessionFactory = $injector.get('SessionFactory');
                });

                afterInjects.forEach(function (afterInject) {
                    afterInject();
                });
            };

        this.afterInjects = afterInjects;
        this.data = data;
        this.mocks = mocks;
        this.injectFactory = injectFactory;
    });

    beforeEach(function () {
        this.afterInjects.push(function () {
            test.results = null;
            test.resultsResolved = true;
        });
    });

    describe('isAuthenticated() and getSession() tests', function () {

        it('isAuthenticated() does not call server side', function () {
            test.injectFactory();

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();
            expect(test.mocks.SessionService.get).not.toHaveBeenCalled();
        });

        it('isAuthenticated() always false while user is not logged in', function () {
            var promise;
            test.injectFactory();
            test.results = test.data.unauthorizedResponse;
            test.resultsResolved = false;

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();

            promise = test.SessionFactory.getSession();
            expect(promise).toBeRejectedWith(test.data.unauthorizedSession);

            expect(test.mocks.SessionService.get).toHaveBeenCalled();
            expect(test.mocks.SessionService.post).not.toHaveBeenCalled();
            expect(test.mocks.SessionService.remove).not.toHaveBeenCalled();
            expect(test.mocks.CommonFactory.showResponseError).not.toHaveBeenCalled();

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();
        });

        it('getSession() can handle unknown errors', function () {
            var promise;
            test.injectFactory();
            test.results = test.data.unknownResponse;
            test.resultsResolved = false;

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();

            promise = test.SessionFactory.getSession();
            expect(promise).toBeRejectedWith(test.data.unauthorizedSession);

            expect(test.mocks.SessionService.get).toHaveBeenCalled();
            expect(test.mocks.SessionService.post).not.toHaveBeenCalled();
            expect(test.mocks.SessionService.remove).not.toHaveBeenCalled();
            expect(test.mocks.CommonFactory.showResponseError).toHaveBeenCalledWith(test.data.unknownResponse);

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();
        });

        it('getSession() get an alive session', function () {
            var promise;
            test.injectFactory();
            test.results = test.data.authorizedByFooSession;

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();

            promise = test.SessionFactory.getSession();
            expect(promise).toBeResolvedWith(test.data.authorizedByFooSession);

            expect(test.mocks.SessionService.get).toHaveBeenCalled();
            expect(test.mocks.SessionService.post).not.toHaveBeenCalled();
            expect(test.mocks.SessionService.remove).not.toHaveBeenCalled();
            expect(test.mocks.CommonFactory.showResponseError).not.toHaveBeenCalled();

            expect(test.SessionFactory.isAuthenticated()).toBeTruthy();
        });

        describe('caching', function () {

            it('cache rejected sessions', function () {
                var promise;
                test.injectFactory();
                test.results = test.data.unauthorizedResponse;
                test.resultsResolved = false;

                promise = test.SessionFactory.getSession();
                expect(promise).toBeRejectedWith(test.data.unauthorizedSession);
                expect(test.mocks.SessionService.get).toHaveBeenCalled();

                test.mocks.SessionService.get.calls.reset();
                promise = test.SessionFactory.getSession();
                expect(promise).toBeRejectedWith(test.data.unauthorizedSession);
                expect(test.mocks.SessionService.get).not.toHaveBeenCalled();
            });

            it('cache resolved sessions', function () {
                var promise;
                test.injectFactory();
                test.results = test.data.authorizedByFooSession;

                promise = test.SessionFactory.getSession();
                expect(promise).toBeResolvedWith(test.data.authorizedByFooSession);
                expect(test.mocks.SessionService.get).toHaveBeenCalled();

                test.mocks.SessionService.get.calls.reset();
                promise = test.SessionFactory.getSession();
                expect(promise).toBeResolvedWith(test.data.authorizedByFooSession);
                expect(test.mocks.SessionService.get).not.toHaveBeenCalled();

            });
        });
    });

    describe('login()', function () {

        it('can login from unauthenticated state and getSession() will returns from cache', function () {
            var promise;
            test.injectFactory();
            test.results = test.data.authorizedByFooSession;

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();

            promise = test.SessionFactory.login('foo', 'bar', false);
            expect(promise).toBeResolvedWith(test.data.authorizedByFooSession);

            expect(test.mocks.SessionService.get).not.toHaveBeenCalled();
            expect(test.mocks.SessionService.post).toHaveBeenCalledWith({
                'username': 'foo',
                'password': 'bar',
                'remember': false
            });
            expect(test.mocks.SessionService.remove).not.toHaveBeenCalled();

            expect(test.SessionFactory.isAuthenticated()).toBeTruthy();

            promise = test.SessionFactory.getSession();
            expect(promise).toBeResolvedWith(test.data.authorizedByFooSession);
            expect(test.mocks.SessionService.get).not.toHaveBeenCalled();
        });

        it('can re-login an authenticated user', function () {
            var promise;
            test.injectFactory();
            test.results = test.data.authorizedByFooSession;

            test.SessionFactory.getSession();
            test.$rootScope.$apply();
            expect(test.SessionFactory.isAuthenticated()).toBeTruthy();
            test.mocks.SessionService.get.calls.reset();

            test.results = test.data.authorizedByBarSession;
            promise = test.SessionFactory.login('bar', 'foo', false);
            expect(promise).toBeResolvedWith(test.data.authorizedByBarSession);

            expect(test.mocks.SessionService.get).not.toHaveBeenCalled();
            expect(test.mocks.SessionService.post).toHaveBeenCalledWith({
                'username': 'bar',
                'password': 'foo',
                'remember': false
            });
            expect(test.mocks.SessionService.remove).not.toHaveBeenCalled();

            expect(test.SessionFactory.isAuthenticated()).toBeTruthy();

            promise = test.SessionFactory.getSession();
            expect(promise).toBeResolvedWith(test.data.authorizedByBarSession);
            expect(test.mocks.SessionService.get).not.toHaveBeenCalled();
        });

        it('show error message when can not login', function () {
            var promise;
            test.injectFactory();
            test.resultsResolved = false;

            test.results = test.data.unknownResponse;
            promise = test.SessionFactory.login('foo', 'bar', false);
            expect(promise).toBeRejectedWith(test.data.unknownResponse);
            expect(test.mocks.SessionService.post).toHaveBeenCalledWith({
                'username': 'foo',
                'password': 'bar',
                'remember': false
            });
            expect(test.mocks.CommonFactory.showResponseError).toHaveBeenCalledWith(test.data.unknownResponse);

            test.mocks.CommonFactory.showResponseError.calls.reset();
            test.mocks.SessionService.post.calls.reset();

            test.results = test.data.unauthorizedResponse;
            promise = test.SessionFactory.login('foo', 'bar', false);
            expect(promise).toBeRejectedWith(test.data.unauthorizedResponse);
            expect(test.mocks.SessionService.post).toHaveBeenCalledWith({
                'username': 'foo',
                'password': 'bar',
                'remember': false
            });
            expect(test.mocks.CommonFactory.showResponseError).toHaveBeenCalledWith(test.data.unauthorizedResponse);
        });
    });

    describe('logout()', function () {

        it('can exec server side logout when user is not logged in client side', function () {
            var promise;
            test.injectFactory();

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();

            promise = test.SessionFactory.logout();
            expect(promise).toBeResolvedWith(test.data.unauthorizedSession);

            expect(test.SessionFactory.isAuthenticated()).toBeFalsy();
            expect(test.mocks.CommonFactory.showResponseError).not.toHaveBeenCalled();
        });

        describe('with client side logged in user', function () {
            beforeEach(function () {
                this.afterInjects.push(function () {
                    test.results = test.data.authorizedByFooSession;
                    test.resultsResolved = true;
                });

                test.injectFactory();

                test.SessionFactory.getSession();
                test.$rootScope.$apply();
                expect(test.SessionFactory.isAuthenticated()).toBeTruthy();

                test.mocks.SessionService.get.calls.reset();
            });

            it('can exec server side logout when user is logged in client side too', function () {
                var promise;

                promise = test.SessionFactory.logout();
                expect(promise).toBeResolvedWith(test.data.unauthorizedSession);

                expect(test.SessionFactory.isAuthenticated()).toBeFalsy();
                expect(test.mocks.CommonFactory.showResponseError).not.toHaveBeenCalled();
            });

            it('handle logout error when user is not loggen in server side', function () {
                var promise;

                test.results = test.data.unauthorizedResponse;
                test.resultsResolved = false;

                promise = test.SessionFactory.logout();
                expect(promise).toBeResolvedWith(test.data.unauthorizedSession);

                expect(test.SessionFactory.isAuthenticated()).toBeFalsy();
                expect(test.mocks.CommonFactory.showResponseError).not.toHaveBeenCalled();
            });

            it('handle unknown logout error without loosing session', function () {
                var promise;

                test.results = test.data.unknownResponse;
                test.resultsResolved = false;

                promise = test.SessionFactory.logout();
                expect(promise).toBeRejectedWith(test.data.unknownResponse);

                expect(test.SessionFactory.isAuthenticated()).toBeTruthy();
                expect(test.mocks.CommonFactory.showResponseError).toHaveBeenCalled();
            });
        });
    });
});
