'use strict';

var appItemViewControllers = angular.module('appControllers.views.item', []);


appItemViewControllers.controller('ItemsController', ['$scope', '$location', '$modal', 'ItemService', 'CommonFactory',
    function ItemsController ($scope, $location, $modal, ItemService, CommonFactory) {
        var modalId = 'item';

        function openItem(item) {
            var newScope = $scope.$new();
            newScope.rowData = item;
            newScope.modalId = modalId;

            $modal({
                'id': modalId,
                'templateUrl': 'partials/views/item.html',
                'scope': newScope,
                'show': true
            });
            $location.search('id', item.id);
        }

        $scope.$on('modal.hide', function (event, $modal) {
            if ($modal.$id === modalId) {
                $location.search('id', null);
            }
        });

        CommonFactory.handlePromise(
            ItemService.getList(),
            'loadingItems',
            function (items) {
                var item = CommonFactory.getObjectById(items, $location.search().id);
                if (item) {
                    openItem(item);
                }
                $scope.items = items;
            });

        $scope.openItem = openItem;
    }]);


appItemViewControllers.controller('ItemController', ['$scope', 'Restangular', 'VendorService', 'UnitService', 'CommonFactory',
    function ItemController ($scope, Restangular, VendorService, UnitService, CommonFactory) {
        function createVendor() {
            var completedNewVendor = {'name': $scope.item.vendor};

            CommonFactory.handlePromise(
                VendorService.post(Restangular.copy(completedNewVendor)),
                'creatingVendor',
                function (resp) {
                    $scope.vendors.push(resp);
                    $scope.item.vendor = resp;
                });
        }

        function createUnit() {
            var completedNewUnit = { 'unit': $scope.item.unit };

            CommonFactory.handlePromise(
                UnitService.post(Restangular.copy(completedNewUnit)),
                'creatingUnit',
                function (resp) {
                    $scope.units.push(resp);
                    $scope.item.unit = resp;
                });
        }

        function saveChanges() {
            $scope.$broadcast('show-errors-check-validity');
            if (!$scope.itemForm.$dirty || !$scope.itemForm.$valid) {
                return;
            }

            CommonFactory.handlePromise(
                $scope.item.put(),
                'savingItem',
                function () {
                    angular.merge($scope.rowData, $scope.item);
                    $scope.itemForm.$setPristine();
                    $scope.$hide();
                });
        }

        function discardChanges() {
            $scope.itemForm.$setPristine();
            $scope.$hide();
        }

        function downloadLabel(barcodeId) {
            window.location.href = 'api/items/' + $scope.item.id + '/barcodes/' + barcodeId + '/print';
            //console.log($scope.item.one('barcodes', barcodeId));
        }

        $scope.item = Restangular.copy($scope.rowData);

        CommonFactory.handlePromise(
            $scope.item.getList('barcodes'),
            'loadingBarcodes',
            function (barcodes) {
                $scope.barcodes = barcodes;
            });

        CommonFactory.handlePromise(
            VendorService.getList(),
            'loadingVendors',
            function (vendors) {
                $scope.vendors = vendors;
            });

        CommonFactory.handlePromise(
            UnitService.getList(),
            'loadingUnits',
            function (units) {
                $scope.units = units;
            });

        $scope.createVendor = createVendor;
        $scope.createUnit = createUnit;
        $scope.downloadLabel = downloadLabel;
        $scope.saveChanges = saveChanges;
        $scope.discardChanges = discardChanges;
    }]);
