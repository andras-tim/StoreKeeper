'use strict';

var appFieldsDirectives = angular.module('appDirectives.fields', []);


/**
 * @ngdoc directive
 * @name appVendorInput
 * @restrict E
 *
 * @param {object} aModel
 *
 * @description
 * Self-managed vendor controller
 *
 * @example
 * <app-input-form a-label="{{ 'Vendor' | translate }}" a-required="{{ 'Vendor is required' | translate }}">
 *   <app-vendor-input a-model="item.vendor"></app-vendor-input>
 * </app-input-form>
 */
appFieldsDirectives.directive('appVendorInput',
    function appVendorInput () {
        return {
            'restrict': 'E',
            'scope': {
                'aModel': '='
            },
            'templateUrl': 'partials/widgets/fields/vendor-input.html',
            'controller': ['$scope', 'Restangular', 'VendorService', 'CommonFactory',
                function ($scope, Restangular, VendorService, CommonFactory) {
                    $scope.data = {};

                    function createVendor() {
                        var completedNewVendor = {'name': $scope.data.vendor};

                        CommonFactory.handlePromise(
                            VendorService.post(Restangular.copy(completedNewVendor)),
                            'creatingVendor',
                            function (resp) {
                                $scope.data.vendorList.push(resp);
                                $scope.data.vendor = resp;
                            });
                    }

                    CommonFactory.handlePromise(
                        VendorService.getList(),
                        'loadingVendors',
                        function (vendors) {
                            $scope.data.vendorList = vendors;
                        });

                    $scope.data.vendor = $scope.aModel;
                    $scope.createVendor = createVendor;
                }]
        };
    });


/**
 * @ngdoc directive
 * @name appUnitInput
 * @restrict E
 *
 * @param {object} aModel
 *
 * @description
 * Self-managed unit controller
 *
 * @example
 * <app-input-form a-label="{{ 'Unit' | translate }}" a-required="{{ 'Unit is required' | translate }}">
 *   <app-unit-input a-model="item.unit"></app-unit-input>
 * </app-input-form>
 */
appFieldsDirectives.directive('appUnitInput',
    function appUnitInput () {
        return {
            'restrict': 'E',
            'scope': {
                'aModel': '='
            },
            'templateUrl': 'partials/widgets/fields/unit-input.html',
            'controller': ['$scope', 'Restangular', 'UnitService', 'CommonFactory',
                function ($scope, Restangular, UnitService, CommonFactory) {
                    $scope.data = {};

                    function createUnit() {
                        var completedNewUnit = {'unit': $scope.data.unit};

                        CommonFactory.handlePromise(
                            UnitService.post(Restangular.copy(completedNewUnit)),
                            'creatingUnit',
                            function (resp) {
                                $scope.data.unitList.push(resp);
                                $scope.data.unit = resp;
                            });
                    }

                    CommonFactory.handlePromise(
                        UnitService.getList(),
                        'loadingUnits',
                        function (units) {
                            $scope.data.unitList = units;
                        });

                    $scope.data.unit = $scope.aModel;
                    $scope.createUnit = createUnit;
                }]
        };
    });


/**
 * @ngdoc directive
 * @name appQuantityInput
 * @restrict E
 *
 * @param {object} aModel
 * @param {func} aOnChange
 *
 * @description
 * Quantity input field
 *
 * @example
 * <app-quantity-input a-model="barcode.quantity" a-on-change="setBarcodeDirty(barcode, true)"></app-quantity-input>
 */
appFieldsDirectives.directive('appQuantityInput',
    function appQuantityInput () {
        return {
            'restrict': 'E',
            'scope': {
                'aModel': '=',
                'aOnChange': '&'
            },
            'templateUrl': 'partials/widgets/fields/quantity-input.html'
        };
    });
