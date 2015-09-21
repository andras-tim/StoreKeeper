'use strict';

var appItemSidebarControllers = angular.module('appControllers.sidebar.item', []);


appItemSidebarControllers.controller('ItemSidebarController', ['$rootScope', '$scope', '$q', '$window', 'gettextCatalog', 'Restangular', 'ItemService', 'BarcodeService', 'CommonFactory', 'PersistFactory',
    function ItemSidebarController ($rootScope, $scope, $q, $window, gettextCatalog, Restangular, ItemService, BarcodeService, CommonFactory, PersistFactory) {
        var persistentStorage = PersistFactory.load('sidebar_item', 1),
            data = persistentStorage.data,
            barcodeCache;

        function addNewBarcode() {
            getBarcode($scope.barcode).then(
                handleExistingBarcode,
                handleNewBarcode
            );
            $scope.barcode = '';
        }

        function handleExistingBarcode(barcode) {
            getItemByBarcode(barcode).then(
                function (item) {
                    var index = _.findIndex(data.readItems, 'id', item.id);
                    if (index >= 0) {
                        addItemQuantity(index, barcode.quantity);
                    } else {
                        data.readItems.push({
                            'id': item.id,
                            'item': item,
                            'quantity': barcode.quantity
                        });
                    }
                    persistentStorage.save();
                }
            );
        }

        function handleNewBarcode(barcodeValue) {
            var index = _.findIndex(data.readItems, {'id': null, 'barcode': barcodeValue});
            if (index >= 0) {
                addItemQuantity(index, 1);
            } else {
                data.readItems.push({
                    'id': null,
                    'barcode': barcodeValue,
                    'quantity': 1
                });
            }
            persistentStorage.save();
        }

        function addItemQuantity(itemIndex, quantity) {
            if (data.ui.summarizeMultipleItems) {
                data.readItems[itemIndex].quantity += quantity;
            }
        }

        function getBarcodes() {
            var result = $q.defer();

            if (angular.isDefined(barcodeCache)) {
                result.resolve(barcodeCache);
                return result.promise;
            }

            CommonFactory.handlePromise(
                BarcodeService.getList(),
                'loadingBarcodes',
                function (barcodes) {
                    barcodeCache = Restangular.stripRestangular(barcodes);
                    result.resolve(barcodeCache);
                });
            return result.promise;
        }

        function getBarcode(barcodeValue) {
            var result = $q.defer();

            getBarcodes().then(function (barcodes) {
                var index = _.findIndex(barcodes, 'barcode', barcodeValue);
                if (index === -1) {
                    result.reject(barcodeValue);
                    return;
                }
                result.resolve(barcodes[index]);
            });

            return result.promise;
        }

        function getItemByBarcode(barcode) {
            var result = $q.defer();

            CommonFactory.handlePromise(
                ItemService.one(barcode.item_id).get(),
                'loadingBarcodesItem',
                function (item) {
                    result.resolve(Restangular.stripRestangular(item));
                },
                function () {
                    result.reject();
                }
            );

            return result.promise;
        }

        function clearReadItems() {
            var message = gettextCatalog.getString('Do you want to clear item list?');
            if ($window.confirm(message)) {
                data.readItems.splice(0, data.readItems.length);
                persistentStorage.save();
            }
        }

        if (!data.readItems) {
            data.readItems = [];
        }
        if (!data.ui) {
            data.ui = {
                'summarizeMultipleItems': true
            };
        }
        $scope.readItems = data.readItems;
        $scope.ui = data.ui;
        $scope.barcode = '';

        $scope.save = persistentStorage.save;
        $scope.addNewBarcode = addNewBarcode;
        $scope.clearReadItems = clearReadItems;
    }]);
