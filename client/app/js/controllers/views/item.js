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
                CommonFactory.handlePromise(
                    ItemService.post(Restangular.copy($scope.item)),
                    null,
                    function (resp) {
                        $scope.item = resp;
                        $scope.itemForm.$setPristine();
                        $scope.barcodes = Restangular.restangularizeCollection($scope.item, $scope.barcodes, 'barcodes');
                        result.resolve();
                    }, function () {
                        result.reject();
                    });
                return promise;
            }

            return CommonFactory.handlePromise(
                $scope.item.put(),
                null,
                function () {
                    angular.merge($scope.elementData, $scope.item);
                    $scope.itemForm.$setPristine();
                });
        }

        function saveBarcodesChanges() {
            var result = $q.defer(),
                promise = result.promise,
                bulkPromises;

            if (!$scope.barcodesForm.$dirty) {
                result.resolve();
                return promise;

            } else if (!$scope.barcodesForm.$valid) {
                result.reject();
                return promise;
            }

            bulkPromises = [];

            promise = deleteBarcodes();
            bulkPromises.push(promise);

            promise = promise.then(updateNonMasterBarcodes);
            bulkPromises.push(promise);

            promise = promise.then(updateMasterBarcodes);
            bulkPromises.push(promise);

            promise = promise.then(createNewBarcodes);
            bulkPromises.push(promise);

            return $q.all(bulkPromises).then(function () {
                $scope.barcodesForm.$setPristine();
            });
        }

        function deleteBarcodes() {
            var index,
                barcode,
                promises = [],

                onDeleteFactory = function onDeleteFactory (index) {
                    return function onDelete () {
                        delete $scope.barcodes[index];
                    };
                };

            for (index = $scope.barcodes.length - 1; index >= 0; index -= 1) {
                barcode = $scope.barcodes[index];

                if (barcode !== undefined && barcode.dirty === 'deleted') {
                    promises.push(
                        CommonFactory.handlePromise(
                            barcode.remove(),
                            null,
                            onDeleteFactory(index)));
                }
            }

            return $q.all(promises);
        }

        function updateNonMasterBarcodes() {
            var length = $scope.barcodes.length,
                index,
                barcode,
                promises = [],

                onUpdateFactory = function onUpdateFactory (barcodeIndex) {
                    return function onUpdate (newBarcode) {
                        $scope.barcodes[barcodeIndex] = newBarcode;
                    };
                };

            for (index = 0; index < length; index += 1) {
                barcode = $scope.barcodes[index];

                if (barcode !== undefined && barcode.dirty === 'modified' && !barcode.master) {
                    promises.push(
                        CommonFactory.handlePromise(
                            barcode.put(),
                            null,
                            onUpdateFactory(index)));
                }
            }

            return $q.all(promises);
        }

        function updateMasterBarcodes() {
            var length = $scope.barcodes.length,
                index,
                barcode,
                promises = [],

                onUpdateFactory = function onUpdateFactory (barcodeIndex) {
                    return function onUpdate (newBarcode) {
                        $scope.barcodes[barcodeIndex] = newBarcode;
                    };
                };

            for (index = 0; index < length; index += 1) {
                barcode = $scope.barcodes[index];

                if (barcode !== undefined && barcode.dirty === 'modified' && barcode.master) {
                    promises.push(
                        CommonFactory.handlePromise(
                            barcode.put(),
                            null,
                            onUpdateFactory(index)));
                }
            }

            return $q.all(promises);
        }

        function createNewBarcodes() {
            var length = $scope.barcodes.length,
                index,
                barcode,
                promises = [],

                onCreateFactory = function onCreateFactory (barcodeIndex) {
                    return function onCreate (newBarcode) {
                        $scope.barcodes[barcodeIndex] = newBarcode;
                    };
                };

            for (index = 0; index < length; index += 1) {
                barcode = $scope.barcodes[index];

                if (barcode !== undefined && barcode.dirty === 'new') {
                    promises.push(
                        CommonFactory.handlePromise(
                            $scope.barcodes.post(Restangular.copy(barcode)),
                            null,
                            onCreateFactory(index)));
                }
            }

            return $q.all(promises);
        }

        function closeModal() {
            $scope.$hide();
        }

        function addNewBarcode(barcodeValue) {
            var newBarcode = {
                'quantity': 1,
                'master': !hasMasterBarcode(),
                'dirty': 'new',
                'labelCommandsDisabled': true
            };
            if (barcodeValue === undefined) {
                newBarcode.main = true;
            } else {
                newBarcode.barcode = barcodeValue;
            }

            $scope.barcodes.push(newBarcode);
            $scope.barcodesForm.$setDirty();
        }

        function hasMasterBarcode() {
            var barcodes = $scope.barcodes,
                length = barcodes.length,
                index,
                barcode;

            for (index = 0; index < length; index += 1) {
                barcode = barcodes[index];
                if (barcode !== undefined && barcode.status !== 'deleted' && barcode.master) {
                    return true;
                }
            }

            return false;
        }

        function setBarcodeDirty(barcode, disableLabelCommands) {
            if (!barcode) {
                return;
            }
            if (barcode.dirty !== 'new') {
                barcode.dirty = 'modified';
            }
            if (disableLabelCommands) {
                barcode.labelCommandsDisabled = true;
            }
        }

        function availableOnlyFilter(barcode) {
            return barcode.dirty !== 'deleted';
        }

        function printLabel(barcode) {
            CommonFactory.handlePromise(
                barcode.customPUT(null, 'print'),
                'printingBarcode'
            );
        }

        function downloadLabel(barcode) {
            $window.location.href = 'api/items/' + $scope.item.id + '/barcodes/' + barcode.id + '/print';
        }

        function deleteBarcode(barcode) {
            var message;

            if (barcode.barcode) {
                message = gettextCatalog.getString(
                    'Do you want to delete barcode {{ barcode }} ({{ quantity }} {{ unit }})', {
                        'barcode': barcode.barcode,
                        'quantity': barcode.quantity,
                        'unit': $scope.item.unit.unit
                    });
            } else {
                message = gettextCatalog.getString(
                    'Do you want to delete new barcode ({{ quantity }} {{ unit }})', {
                        'quantity': barcode.quantity,
                        'unit': $scope.item.unit.unit
                    });
            }

            if ($window.confirm(message)) {
                $scope.barcodesForm.$setDirty();

                if (barcode.dirty === 'new') {
                    _.remove($scope.barcodes, function (currentBarcode) {
                        return currentBarcode === barcode;
                    });
                } else {
                    barcode.dirty = 'deleted';
                }
            }
        }

        function togglePostCheck(currentBarcode) {
            if (!currentBarcode.master) {
                return;
            }
            _.forEach($scope.barcodes, function (barcode) {
                if ((barcode !== undefined) && barcode.dirty !== 'deleted' && barcode.master && (barcode !== currentBarcode)) {
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
                'purchase_price': 0,
                'unit': {},
                'vendor': {}
            };
            $scope.barcodes = [];

            $timeout(function () {
                if ($scope.elementData.new.barcode) {
                    addNewBarcode($scope.elementData.new.barcode);
                } else {
                    addNewBarcode();
                }
            });
        }

        function fetchBarcodes() {
            CommonFactory.handlePromise(
                $scope.item.getList('barcodes'),
                'loadingBarcodes',
                function (barcodes) {
                    $scope.barcodes = barcodes;
                });
        }

        if ($scope.elementData.new) {
            prepareScopeForNewItem();

        } else {
            $scope.item = Restangular.copy($scope.elementData);
            fetchBarcodes();
        }

        $scope.availableOnlyFilter = availableOnlyFilter;
        $scope.addNewBarcode = addNewBarcode;
        $scope.setBarcodeDirty = setBarcodeDirty;
        $scope.togglePostCheck = togglePostCheck;
        $scope.printLabel = printLabel;
        $scope.downloadLabel = downloadLabel;
        $scope.deleteBarcode = deleteBarcode;
        $scope.saveChanges = saveChanges;
        $scope.closeModal = closeModal;
    }]);
