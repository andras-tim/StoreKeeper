'use strict';

describe('ItemController', function () {
    var test;

    beforeEach(module('appControllers'));

    beforeEach(function () {
        test = this;

        var beforeInjects = [],

            data = {
                'item': {
                    'article_number': 1234,
                    'id': 1,
                    'name': 'Orange',
                    'quantity': 10,
                    'unit': {
                        'id': 2,
                        'unit': 'kg'
                    },
                    'vendor': {
                        'id': 3,
                        'name': 'Foo Bar'
                    }
                },
                'vendors': [
                    {
                        'id': 3,
                        'name': 'Foo Bar.'
                    },
                    {
                        'id': 4,
                        'name': 'Kiwi Co.'
                    }],
                'units': [
                    {
                        'id': 5,
                        'unit': 'pcs'
                    },
                    {
                        'id': 2,
                        'unit': 'kg'
                    }],
                'barcodes': [
                    {
                        'barcode': 'SK227571',
                        'id': 46,
                        'main': true,
                        'quantity': 1
                    },
                    {
                        'barcode': 'SK665157',
                        'id': 47,
                        'main': false,
                        'quantity': 15
                    }
                ]
            },

            mocks = {
                '$scope': {
                    '$hide': function () {},
                    'rowData': {
                        'put': function (item) {
                            return helper.promiseMock(test, 'itemPutResolved', item);
                        },
                        'getList': function () {
                            return helper.promiseMock(test, 'itemGetListResolved', mocks.barcodeList);
                        }
                    }
                },
                'Restangular': {
                    'copy': function (data) {
                        return angular.extend({}, data);
                    }
                },
                'vendorList': angular.extend({
                    'push': function () {}
                }, data.vendors),
                'VendorService': {
                    'getList': function () {
                        return helper.promiseMock(test, 'vendorsGetListResolved', mocks.vendorList);
                    },
                    'post': function (newVendor) {
                        return helper.promiseMock(test, 'vendorPostResolved', newVendor);
                    }
                },
                'unitList': angular.extend({
                    'push': function () {}
                }, data.units),
                'UnitService': {
                    'getList': function () {
                        return helper.promiseMock(test, 'unitsGetListResolved', mocks.unitList);
                    },
                    'post': function (newUnit) {
                        return helper.promiseMock(test, 'unitPostResolved', newUnit);
                    }
                },
                'barcodeList': angular.extend({
                    'push': function () {}
                }, data.barcodes),
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
                spyOn(test.mocks.$scope, '$hide').and.stub();
                spyOn(test.mocks.$scope.rowData, 'put').and.callThrough();
                spyOn(test.mocks.$scope.rowData, 'getList').and.callThrough();
                spyOn(test.mocks.Restangular, 'copy').and.callThrough();
                spyOn(test.mocks.VendorService, 'getList').and.callThrough();
                spyOn(test.mocks.vendorList, 'push').and.stub();
                spyOn(test.mocks.UnitService, 'getList').and.callThrough();
                spyOn(test.mocks.unitList, 'push').and.stub();

                beforeInjects.forEach(function (beforeInject) {
                    beforeInject();
                });

                inject(function ($controller, $rootScope, $q) {
                    test.$rootScope = $rootScope;
                    test.$q = $q;

                    $controller('ItemController', dependencies);
                });
            };

        this.beforeInjects = beforeInjects;
        this.data = data;
        this.mocks = mocks;
        this.injectController = injectController;
    });

    beforeEach(function () {
        test.itemPutResolved = true;
        test.itemGetListResolved = true;
        test.vendorsGetListResolved = true;
        test.vendorPostResolved = true;
        test.unitsGetListResolved = true;
        test.unitPostResolved = true;

        test.beforeInjects.push(function () {
            angular.merge(test.mocks.$scope.rowData, test.data.item);
        });
    });

    describe('rowData', function () {

        beforeEach(function () {
            test.injectController();
            test.$rootScope.$apply();
        });

        it('pre-test mock', function () {
            expect(test.mocks.Restangular.copy).toHaveBeenCalled();
            expect(test.mocks.$scope.item).toEqual(test.mocks.$scope.rowData);
            expect(test.mocks.$scope.item).not.toBe(test.mocks.$scope.rowData);
        });

        it('rowData does not change until saving', function () {
            test.mocks.$scope.item.name = 'New Name';
            expect(test.mocks.$scope.item).not.toEqual(test.mocks.$scope.rowData);

            test.mocks.$scope.saveChanges();
            test.$rootScope.$apply();
            expect(test.mocks.$scope.item).toEqual(test.mocks.$scope.rowData);
        });
    });

    describe('external resources', function () {

        it('can load', function () {
            test.injectController();
            test.$rootScope.$apply();

            expect(test.mocks.VendorService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.vendors).toBe(test.mocks.vendorList);

            expect(test.mocks.UnitService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.units).toBe(test.mocks.unitList);

            expect(test.mocks.$scope.rowData.getList).toHaveBeenCalledWith('barcodes');
            expect(test.mocks.$scope.barcodes).toBe(test.mocks.barcodeList);
        });

        it('can not load by server error', function () {
            test.vendorsGetListResolved = false;
            test.unitsGetListResolved = false;
            test.itemGetListResolved = false;
            test.injectController();
            test.$rootScope.$apply();

            expect(test.mocks.VendorService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.vendors).not.toBeDefined();

            expect(test.mocks.UnitService.getList).toHaveBeenCalled();
            expect(test.mocks.$scope.units).not.toBeDefined();

            expect(test.mocks.$scope.rowData.getList).toHaveBeenCalledWith('barcodes');
            expect(test.mocks.$scope.barcodes).not.toBeDefined();
        });

        it('can save then closes window', function () {
            test.injectController();
            test.$rootScope.$apply();

            test.mocks.$scope.item.name = 'New Name';
            test.mocks.$scope.saveChanges();
            test.$rootScope.$apply();

            expect(test.mocks.$scope.rowData.put).toHaveBeenCalled();
            expect(test.mocks.$scope.rowData).toEqual(test.mocks.$scope.item);
            expect(test.mocks.$scope.$hide).toHaveBeenCalled();
        });

        it('can not save', function () {
            test.itemPutResolved = false;
            test.injectController();
            test.$rootScope.$apply();

            test.mocks.$scope.item.name = 'New Name';
            test.mocks.$scope.saveChanges();
            test.$rootScope.$apply();

            expect(test.mocks.$scope.rowData.put).toHaveBeenCalled();
            expect(test.mocks.$scope.rowData).not.toEqual(test.mocks.$scope.item);
            expect(test.mocks.$scope.$hide).not.toHaveBeenCalled();
        });
    });

    describe('create a new vendor', function () {

        beforeEach(function () {
            test.injectController();
            test.$rootScope.$apply();

            test.mocks.$scope.item.vendor = 'New Apple';
        });

        it('can add a new vendor', function () {
            test.mocks.$scope.createVendor();
            test.$rootScope.$apply();

            expect(test.mocks.vendorList.push).toHaveBeenCalledWith({'name': 'New Apple'});
            expect(test.mocks.$scope.item.vendor).toEqual({'name': 'New Apple'});
        });

        it('can not add a new vendor by server error', function () {
            test.vendorPostResolved = false;

            test.mocks.$scope.createVendor();
            test.$rootScope.$apply();

            expect(test.mocks.vendorList.push).not.toHaveBeenCalled();
            expect(test.mocks.$scope.item.vendor).toEqual('New Apple');
        });
    });

    describe('create a new unit', function () {

        beforeEach(function () {
            test.injectController();
            test.$rootScope.$apply();

            test.mocks.$scope.item.unit = 'pcs';
        });

        it('can add a new unit', function () {
            test.mocks.$scope.createUnit();
            test.$rootScope.$apply();

            expect(test.mocks.unitList.push).toHaveBeenCalledWith({'unit': 'pcs'});
            expect(test.mocks.$scope.item.unit).toEqual({'unit': 'pcs'});
        });

        it('can not add a new unit by server error', function () {
            test.unitPostResolved = false;

            test.mocks.$scope.createUnit();
            test.$rootScope.$apply();

            expect(test.mocks.unitList.push).not.toHaveBeenCalled();
            expect(test.mocks.$scope.item.unit).toEqual('pcs');
        });
    });
});
