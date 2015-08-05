'use strict';

describe('UserMenuController', function () {
    var test;

    beforeEach(module('appControllers'));

    beforeEach(function () {
        test = this;

        var mocks = {
                '$location': {
                    'path': function () {}
                },
                'SessionFactory': {
                    'logout': function () {
                        var deferred = test.$q.defer();
                        if (test.logoutResolved) {
                            deferred.resolve();
                        } else {
                            deferred.reject();
                        }
                        return deferred.promise;
                    }
                },
                'CommonFactory': {
                    'handlePromise': function (promise, spinner, resolve, reject) {
                        promise.then(resolve, reject);
                    }
                }
            },

            dependencies = {
                '$location': mocks.$location,
                'SessionFactory': mocks.SessionFactory,
                'CommonFactory': mocks.CommonFactory
            },

            injectController = function () {
                spyOn(mocks.$location, 'path').and.stub();
                spyOn(mocks.SessionFactory, 'logout').and.callThrough();

                inject(function ($controller, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$scope = $rootScope.$new();
                    test.$q = $q;

                    dependencies.$scope = test.$scope;

                    $controller('UserMenuController', dependencies);
                });
            };

        this.mocks = mocks;
        this.injectController = injectController;
    });

    beforeEach(function () {
        test.logoutResolved = true;
    });

    it('check interface', function () {
        test.injectController();

        expect(test.$scope.logout).toBeDefined();
    });

    describe('logout()', function () {
        it('have to log out on server side, and redirect to login page', function () {
            test.injectController();

            test.$scope.logout();
            test.$rootScope.$apply();

            expect(test.mocks.SessionFactory.logout).toHaveBeenCalled();
            expect(test.mocks.$location.path).toHaveBeenCalledWith('/login');
        });

        it('do nothing when logout() was failed', function () {
            test.logoutResolved = false;
            test.injectController();

            test.$scope.logout();
            test.$rootScope.$apply();

            expect(test.mocks.SessionFactory.logout).toHaveBeenCalled();
            expect(test.mocks.$location.path).not.toHaveBeenCalled();
        });
    });
});
