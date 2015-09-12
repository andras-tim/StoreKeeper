'use strict';

describe('LoginController', function () {
    var test;

    beforeEach(module('appControllers'));

    beforeEach(function () {
        test = this;

        var data = {
                'userFormWithoutRemember': {
                    'username': 'foo',
                    'password': 'bar',
                    'remember': false
                },
                'userFormWithRemember': {
                    'username': 'foo2',
                    'password': 'bar2',
                    'remember': true
                }
            },

            mocks = {
                '$scope': {
                    '$broadcast': function () {},
                    'userForm': {
                        '$valid': true,
                        '$setPristine': function () {}
                    }
                },
                '$location': {
                    'path': function () {}
                },
                'SessionFactory': {
                    'login': function () {
                        return helper.promiseMock(test, 'loginResolved');
                    }
                },
                'CommonFactory': {
                    'handlePromise': function (promise, spinner, resolve, reject) {
                        return promise.then(resolve, reject);
                    }
                }
            },

            dependencies = {
                '$scope': mocks.$scope,
                '$location': mocks.$location,
                'SessionFactory': mocks.SessionFactory,
                'CommonFactory': mocks.CommonFactory
            },

            injectController = function () {
                spyOn(mocks.$scope, '$broadcast').and.callThrough();
                spyOn(mocks.$scope.userForm, '$setPristine').and.stub();
                spyOn(mocks.$location, 'path').and.stub();
                spyOn(mocks.SessionFactory, 'login').and.callThrough();
                spyOn(mocks.CommonFactory, 'handlePromise').and.callThrough();

                inject(function ($controller, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$q = $q;

                    $controller('LoginController', dependencies);
                });

                test.$rootScope.$apply();
            };

        this.data = data;
        this.mocks = mocks;
        this.injectController = injectController;
    });

    beforeEach(function () {
        test.loginResolved = true;
    });

    it('test interface', function () {
        test.injectController();

        expect(test.mocks.$scope.login).toBeDefined();
        expect(test.mocks.$scope.user).toBeDefined();
    });

    describe('login()', function () {

        it('have to check form, login on server side and redirect to main page', function () {
            test.injectController();

            test.mocks.$scope.login();
            test.$rootScope.$apply();

            expect(test.mocks.$scope.$broadcast).toHaveBeenCalledWith('show-errors-check-validity');
            expect(test.mocks.SessionFactory.login).toHaveBeenCalled();
            expect(test.mocks.$scope.userForm.$setPristine).toHaveBeenCalled();
            expect(test.mocks.$location.path).toHaveBeenCalledWith('/');
        });

        describe('user fields have to push to server side', function () {
            var user;

            beforeEach(function () {
                test.injectController();
            });

            afterEach(function () {
                test.mocks.$scope.user = user;
                test.mocks.$scope.login();
                test.$rootScope.$apply();
                expect(test.mocks.SessionFactory.login).
                    toHaveBeenCalledWith(user.username, user.password, user.remember);
            });

            it('foo; without remember', function () {
                user = test.data.userFormWithoutRemember;

            });

            it('foo2; with remember', function () {
                user = test.data.userFormWithRemember;

            });
        });

        it('invalid form have to abort login process', function () {
            test.injectController();
            test.mocks.$scope.userForm.$valid = false;

            test.mocks.$scope.login();

            expect(test.mocks.$scope.$broadcast).toHaveBeenCalledWith('show-errors-check-validity');
            expect(test.mocks.SessionFactory.login).not.toHaveBeenCalled();
            expect(test.mocks.$location.path).not.toHaveBeenCalled();
        });

        it('invalid server response have to hold on login page', function () {
            test.loginResolved = false;
            test.injectController();

            test.mocks.$scope.login();

            expect(test.mocks.$scope.userForm.$setPristine).not.toHaveBeenCalled();
            expect(test.mocks.$location.path).not.toHaveBeenCalled();
        });
    });
});
