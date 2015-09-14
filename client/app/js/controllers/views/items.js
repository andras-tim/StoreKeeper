'use strict';

var appItemViewControllers = angular.module('appControllers.views.items', []);


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
                var index,
                    desiredId = parseInt($location.search().id);

                if (!isNaN(desiredId)) {
                    index = _.findIndex(items, 'id', desiredId);
                    if (index !== -1) {
                        openItem(items[index]);
                    }
                }
                $scope.items = items;
            });

        $scope.openItem = openItem;
    }]);


appItemViewControllers.controller('ItemController', ['$scope', '$window', '$q', 'Restangular', 'gettextCatalog', 'VendorService', 'UnitService', 'CommonFactory',
    function ItemController ($scope, $window, $q, Restangular, gettextCatalog, VendorService, UnitService, CommonFactory) {
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

            CommonFactory.handlePromise(
                saveItemChanges().then(saveBarcodesChanges),
                'savingItem',
                function () {
                    console.log('done');
                });
        }

        function saveItemChanges() {
            var result = $q.defer(),
                promise = result.promise;

            if (!$scope.itemForm.$dirty) {
                result.resolve();
                return promise;

            } else if (!$scope.itemForm.$valid) {
                result.reject();
                return promise;
            }

            return CommonFactory.handlePromise(
                $scope.item.put(),
                null,
                function () {
                    console.log('saving item');
                    angular.merge($scope.rowData, $scope.item);
                    $scope.itemForm.$setPristine();
                });
        }

        function saveBarcodesChanges() {
            var result = $q.defer(),
                promise = result.promise;

            if (!$scope.barcodesForm.$dirty) {
                result.resolve();
                return promise;

            } else if (!$scope.barcodesForm.$valid) {
                result.reject();
                return promise;
            }
            result.resolve();

            if (!$scope.barcodesForm.$dirty || !$scope.barcodesForm.$valid) {
                return;
            }

            _.forEach($scope.barcodes, function (barcode, i) {
                if (barcode.deleted) {
                    console.log('deleting item');
                    promise.then(function () {
                        promise = CommonFactory.handlePromise(
                            barcode.remove(),
                            null,
                            function () {
                                delete $scope.barcodes[i];
                            }
                        );
                    });
                }
            });

            _.forEach($scope.barcodes, function (barcode) {
                if ((barcode !== undefined) && !barcode.deleted && barcode.dirty && !barcode.master) {
                    promise.then(function () {
                        console.log('updating item');
                        promise = CommonFactory.handlePromise(
                            barcode.put(),
                            null,
                            function () {
                                barcode.dirty = false;
                                barcode.dirtyForLabel = false;
                            });
                    });
                }
            });

            _.forEach($scope.barcodes, function (barcode) {
                if ((barcode !== undefined) && !barcode.deleted && barcode.dirty && barcode.master) {
                    promise.then(function () {
                        console.log('updating2 item');
                        promise = CommonFactory.handlePromise(
                            barcode.put(),
                            null,
                            function () {
                                barcode.dirty = false;
                                barcode.dirtyForLabel = false;
                            });
                    });
                }
            });

            return CommonFactory.handlePromise(
                promise,
                null,
                function () {
                    console.log('saving barcodes');
                    $scope.barcodesForm.$setPristine();
                });
        }

        function closeModal() {
            $scope.$hide();
        }

        function createBarcode() {
            var emptyBarcode = {'master': false};

            CommonFactory.handlePromise(
                $scope.barcodes.post(Restangular.copy(emptyBarcode)),
                'creatingBarcode',
                function (resp) {
                    $scope.barcodes.push(resp);
                });
        }

        function setBarcodeDirty(barcode, dirtiedForLabel) {
            if (!barcode) {
                return;
            }
            barcode.dirty = true;
            if (dirtiedForLabel) {
                barcode.dirtyForLabel = true;
            }
        }

        function filterAvailable(barcode) {
            return !barcode.deleted;
        }

        function printLabel(barcode) {
            CommonFactory.handlePromise(
                barcode.customPUT(null, 'print'),
                'printingBarcode'
            );
        }

        function downloadLabel(barcode) {
            window.location.href = 'api/items/' + $scope.item.id + '/barcodes/' + barcode.id + '/print';
        }

        function deleteBarcode(barcode) {
            var message = gettextCatalog.getString(
                'Do you want to delete barcode {{ barcode }} ({{ quantity }} {{ unit }})', {
                    'barcode': barcode.barcode,
                    'quantity': barcode.quantity,
                    'unit': $scope.item.unit.unit
                });

            if ($window.confirm(message)) {
                $scope.barcodesForm.$setDirty();
                barcode.deleted = true;
            }
        }

        function togglePostCheck(currentBarcode) {
            console.log(currentBarcode);

            if (!currentBarcode.master) {
                return;
            }
            _.forEach($scope.barcodes, function (barcode) {
                if ((barcode !== undefined) && !barcode.deleted && barcode.master && (barcode !== currentBarcode)) {
                    barcode.master = false;
                    setBarcodeDirty(barcode);
                }
            });
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
        $scope.createBarcode = createBarcode;
        $scope.filterAvailable = filterAvailable;
        $scope.setBarcodeDirty = setBarcodeDirty;
        $scope.togglePostCheck = togglePostCheck;
        $scope.printLabel = printLabel;
        $scope.downloadLabel = downloadLabel;
        $scope.deleteBarcode = deleteBarcode;
        $scope.saveChanges = saveChanges;
        $scope.closeModal = closeModal;
    }]);
