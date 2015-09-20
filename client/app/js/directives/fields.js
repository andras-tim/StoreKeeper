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
