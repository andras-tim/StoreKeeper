'use strict';

var appViewControllers = angular.module('appControllers.views');


appViewControllers.controller('ItemController', ['$scope', '$window', '$q', '$timeout', 'Restangular', 'gettextCatalog', 'CommonFactory', 'ItemService',
    function ItemController ($scope, $window, $q, $timeout, Restangular, gettextCatalog, CommonFactory, ItemService) {
        function saveChanges() {
            $scope.$broadcast('show-errors-check-validity');

            CommonFactory.handlePromise(
                saveItemChanges().then(saveBarcodesChanges),
                'savingItem',
                function () {
                    if (angular.isDefined($scope.elementData.onSave)) {
                        $timeout(function () {
                            $scope.elementData.onSave($scope.item, $scope.barcodes);
                        });
                    }
                    angular.merge($scope.elementData, $scope.item);
                    $scope.elementData.new = undefined;

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

            if ($scope.elementData.new) {
                return CommonFactory.handlePromise(
                    ItemService.post(Restangular.copy($scope.item)),
                    null,
                    function (resp) {
                        $scope.item = resp;
                        $scope.itemForm.$setPristine();
                    });
            } else {
                return CommonFactory.handlePromise(
                    $scope.item.put(),
                    null,
                    function () {
                        console.log('saving item');
                        angular.merge($scope.elementData, $scope.item);
                        $scope.itemForm.$setPristine();
                    });
            }
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

            if ($scope.elementData.new) {
                return CommonFactory.handlePromise(
                    $scope.item.all('barcodes').post(Restangular.copy($scope.barcodes[0])),
                    'creatingBarcode',
                    function (resp) {
                        angular.merge($scope.barcodes[0], resp);
                    });
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

            return CommonFactory.handlePromise(
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

        function prepareScopeForNewItem() {
            $scope.item = {
                'article_number': '',
                'name': '',
                'warning_quantity': 0,
                'quantity': 0,
                'unit': {},
                'vendor': {}
            };
            $scope.barcodes = [];

            if ($scope.elementData.new.barcode) {
                $scope.barcodes.push({
                    'barcode': $scope.elementData.new.barcode,
                    'quantity': 1,
                    'dirty': true
                });
            } else {
                $scope.barcodes.push({
                    'quantity': 1,
                    'master': true,
                    'dirty': true
                });
            }

            $timeout(function () {
                $scope.barcodesForm.$setDirty();
            });
        }

        if ($scope.elementData.new) {
            prepareScopeForNewItem();

        } else {
            $scope.item = Restangular.copy($scope.elementData);
            CommonFactory.handlePromise(
                $scope.item.getList('barcodes'),
                'loadingBarcodes',
                function (barcodes) {
                    $scope.barcodes = barcodes;
                });
        }

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
