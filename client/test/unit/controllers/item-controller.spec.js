'use strict';

describe('ItemController', function () {
    var test;

    beforeEach(module('appControllers'));

    beforeEach(function () {
        test = this;

        var mocks = {
                '$scope': {},
                'Restangular': {
                    'copy': function (data) {
                        return data;
                    }
                },
                'vendorList': {
                    'push': function () {}
                },
                'VendorService': {
                    'getList': function () {
                        return helper.promiseMock(test, 'vendorsGetListResolved', mocks.vendorList);
                    },
                    'post': function (newVendor) {
                        return helper.promiseMock(test, 'vendorPostResolved', newVendor);
                    }
                },
                'unitList': {
                    'push': function () {}
                },
                'UnitService': {
                    'getList': function () {
                        return helper.promiseMock(test, 'unitsGetListResolved', mocks.unitList);
                    },
                    'post': function (newUnit) {
                        return helper.promiseMock(test, 'unitPostResolved', newUnit);
                    }
                },
                'CommonFactory': {
                    'handlePromise': function (promise, spinner, resolve, reject) {
                        promise.then(resolve, reject);

                    }
                }
            },

            dependencies = {
                '$scope': mocks.$scope,
                'Restangular': mocks.Restangular,
                'VendorService': mocks.VendorService,
                'UnitService': mocks.UnitService,
                'CommonFactory': mocks.CommonFactory
            },

            injectController = function () {
                spyOn(test.mocks.VendorService, 'getList').and.callThrough();
                spyOn(test.mocks.vendorList, 'push').and.stub();
                spyOn(test.mocks.UnitService, 'getList').and.callThrough();
                spyOn(test.mocks.unitList, 'push').and.stub();

                inject(function ($controller, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$q = $q;

                    $controller('ItemController', dependencies);
                });
            };

        this.mocks = mocks;
        this.injectController = injectController;
    });

    beforeEach(function () {
        test.vendorsGetListResolved = true;
        test.vendorPostResolved = true;
        test.unitsGetListResolved = true;
        test.unitPostResolved = true;
    });

    describe('depended items', function () {

        it('can load', function () {
            test.injectController();
            test.$rootScope.$apply();

            expect(test.mocks.VendorService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.vendors).toBe(test.mocks.vendorList);

            expect(test.mocks.UnitService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.units).toBe(test.mocks.unitList);
        });

        it('can not load by server error', function () {
            test.vendorsGetListResolved = false;
            test.unitsGetListResolved = false;
            test.injectController();
            test.$rootScope.$apply();

            expect(test.mocks.VendorService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.vendors).not.toBeDefined();

            expect(test.mocks.UnitService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.units).not.toBeDefined();
        });
    });

    describe('test isFilled() on model values of input box', function () {

        beforeEach(function () {
            test.injectController();
        });

        it('string content means it is not filled', function () {
            expect(test.mocks.$scope.isFilled('')).toBeFalsy();
            expect(test.mocks.$scope.isFilled('foo')).toBeFalsy();
        });

        it('dict content means it is filled', function () {
            expect(test.mocks.$scope.isFilled({})).toBeTruthy();
            expect(test.mocks.$scope.isFilled({'name': 'foo'})).toBeTruthy();
        });
    });

    describe('create a new vendor', function () {

        beforeEach(function () {
            test.injectController();
            test.$rootScope.$apply();

            test.mocks.$scope.vendor = 'New Apple';
        });

        it('can add a new vendor', function () {
            test.mocks.$scope.createVendor();
            test.$rootScope.$apply();

            expect(test.mocks.vendorList.push).toHaveBeenCalledWith({'name': 'New Apple'});
            expect(test.mocks.$scope.vendor).toEqual({'name': 'New Apple'});
        });

        it('can not add a new vendor by server error', function () {
            test.vendorPostResolved = false;

            test.mocks.$scope.createVendor();
            test.$rootScope.$apply();

            expect(test.mocks.vendorList.push).not.toHaveBeenCalled();
            expect(test.mocks.$scope.vendor).toEqual('New Apple');
        });
    });

    describe('create a new unit', function () {

        beforeEach(function () {
            test.injectController();
            test.$rootScope.$apply();

            test.mocks.$scope.unit = 'pcs';
        });

        it('can add a new unit', function () {
            test.mocks.$scope.createUnit();
            test.$rootScope.$apply();

            expect(test.mocks.unitList.push).toHaveBeenCalledWith({'unit': 'pcs'});
            expect(test.mocks.$scope.unit).toEqual({'unit': 'pcs'});
        });

        it('can not add a new unit by server error', function () {
            test.unitPostResolved = false;

            test.mocks.$scope.createUnit();
            test.$rootScope.$apply();

            expect(test.mocks.unitList.push).not.toHaveBeenCalled();
            expect(test.mocks.$scope.unit).toEqual('pcs');
        });
    });
});
