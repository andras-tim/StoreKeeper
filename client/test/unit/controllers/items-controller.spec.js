'use strict';

describe('ItemsController', function () {
    var test;

    beforeEach(module('appControllers'));

    beforeEach(function () {
        test = this;

        var data = {
                'items': ['foo', 'bar']
            },

            mocks = {
                '$scope': {},
                'ItemService': {
                    'getList': function () {
                        return helper.promiseMock(test, 'getListResolved', data.items);
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
                'ItemService': mocks.ItemService,
                'CommonFactory': mocks.CommonFactory
            },

            injectController = function () {
                spyOn(test.mocks.ItemService, 'getList').and.callThrough();

                inject(function ($controller, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$q = $q;

                    $controller('ItemsController', dependencies);
                });
            };

        this.data = data;
        this.mocks = mocks;
        this.injectController = injectController;
    });

    beforeEach(function () {
        test.getListResolved = true;
    });

    it('can get items from server side', function () {
        test.injectController();
        expect(test.mocks.$scope.items).not.toBeDefined();

        test.$rootScope.$apply();

        expect(test.mocks.ItemService.getList).toHaveBeenCalled();
        expect(test.mocks.$scope.items).toEqual(test.data.items);
    });

    it('handle server side errors', function () {
        test.getListResolved = false;
        test.injectController();
        expect(test.mocks.$scope.items).not.toBeDefined();

        test.$rootScope.$apply();

        expect(test.mocks.ItemService.getList).toHaveBeenCalled();
        expect(test.mocks.$scope.items).not.toBeDefined();
    });
});
