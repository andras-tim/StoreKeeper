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
 * <app-input-form a-label="{{ 'Vendor' | translate }}">
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
                    $scope.$watch('data.vendor', function (newVendor) {
                        $scope.aModel = newVendor;
                    });

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
 * <app-input-form a-label="{{ 'Unit' | translate }}">
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
                    $scope.$watch('data.unit', function (newUnit) {
                        $scope.aModel = newUnit;
                    });

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
 * @param {object} aMin
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
            'replace': true,
            'scope': {
                'aModel': '=',
                'aMin': '=',
                'aOnChange': '&'
            },
            'templateUrl': 'partials/widgets/fields/quantity-input.html'
        };
    });


/**
 * @ngdoc directive
 * @name appPurchasePriceInput
 * @restrict E
 *
 * @param {object} aModel
 * @param {object} aMin
 * @param {func} aOnChange
 *
 * @description
 * Purchase price input field
 *
 * @example
 * <app-purchase-price-input a-model="item.purchase_price" a-min="0"></app-purchase-price-input>
 */
appFieldsDirectives.directive('appPurchasePriceInput',
    function appPurchasePriceInput () {
        return {
            'restrict': 'E',
            'replace': true,
            'scope': {
                'aModel': '=',
                'aMin': '=',
                'aOnChange': '&'
            },
            'templateUrl': 'partials/widgets/fields/purchase-price-input.html',
            'controller': ['$scope', 'CommonFactory', 'ConfigFactory',
                function ($scope, CommonFactory, ConfigFactory) {
                    $scope.data = {};

                    CommonFactory.handlePromise(
                        ConfigFactory.getConfig(),
                        'loadingCurrency',
                        function (config) {
                            $scope.data.currency = config.currency;
                        });
                }]
        };
    });


/**
 * @ngdoc directive
 * @name appItemInput
 * @restrict E
 *
 * @param {object} aModel
 * @param {func} aOnChange
 * @param {expression} aAutofocus
 *
 * @description
 * Item selector typeahead (results is not trimmed)
 *
 * @example
 * <app-item-input a-model="data"></app-item-input>
 */
appFieldsDirectives.directive('appItemInput',
    function appItemInput () {
        return {
            'restrict': 'E',
            'scope': {
                'aModel': '=',
                'aOnChange': '&'
            },
            'templateUrl': 'partials/widgets/fields/item-input.html',
            'compile': function (element, attrs) {
                element.find('input').attr('autofocus', angular.isUndefined(attrs.aAutofocus) ? null : '');
            },
            'controller': ['$scope', '$q', '$typeahead', 'ItemService', 'CommonFactory',
                function ($scope, $q, $typeahead, ItemService, CommonFactory) {

                    var dataFetcher = function dataFetcher (filter) {
                            var options = {
                                'expression': filter,
                                'limit': $typeahead.defaults.limit
                            };

                            return CommonFactory.handlePromise(
                                ItemService.one('search').getList(null, options)
                            );
                        },

                        delayedDataFetcher = CommonFactory.createDelayedPromiseCallback(dataFetcher),

                        getData = function getData ($modelValue, $viewValue) {
                            delayedDataFetcher.cancel();
                            if (!$viewValue || angular.isObject($modelValue)) {
                                return;
                            }

                            return delayedDataFetcher.callback($viewValue);
                        };

                    $scope.getData = getData;
                }]
        };
    });
