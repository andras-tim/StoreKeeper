'use strict';

var appItemSidebarControllers = angular.module('appControllers.sidebar.item', []);


appItemSidebarControllers.controller('ItemSidebarController', ['$scope', '$q', '$window', 'gettextCatalog', 'BarcodeCacheFactory', 'ItemService', 'CommonFactory', 'PersistFactory',
    function ItemSidebarController ($scope, $q, $window, gettextCatalog, BarcodeCacheFactory, ItemService, CommonFactory, PersistFactory) {
        var
            /**
             * Persistent storage
             *
             * It can load and save settings of this controller
             */
            persistentStorageClass = function persistentStorageClass () {
                var storage = PersistFactory.load('sidebar_item', 1),
                    data = storage.data;

                if (!data.readItems) {
                    data.readItems = [];
                }

                if (!data.uiSettings) {
                    data.uiSettings = {
                        'summarizeMultipleItems': true
                    };
                }

                return {
                    'data': data,
                    'save': storage.save
                };
            },

            /**
             * Persistable item storage
             *
             * Item structure:
             * {
             *   'item': <Item by ItemService>,
             *   'data': <reference of persisted 'id', 'barcode' 'quantity' contained object>
             * }
             */
            itemListClass = function itemListClass (itemStorage) {
                var items = [],

                fetchItemStorage = function fetchItemStorage () {
                    var length = itemStorage.length,
                        index,
                        readItem;

                    for (index = 0; index < length; index += 1) {
                        readItem = itemStorage.shift();
                        if (readItem.id) {
                            addItem(readItem.id, readItem.quantity);
                        } else {
                            addNewItem(readItem.barcode, readItem.quantity);
                        }
                    }
                },

                addItem = function addItem (itemId, quantity) {
                    var readItem = pushItemData({
                            'id': itemId,
                            'quantity': quantity
                        });

                    getItemById(itemId).then(function (item) {
                        readItem.item = item;
                    });
                },

                addNewItem = function addNewItem (barcode, quantity) {
                    pushItemData({
                        'id': null,
                        'barcode': barcode,
                        'quantity': quantity || 1
                    });
                },

                pushItemData = function pushItemData (itemData) {
                    var readItem = {
                        'item': null,
                        'data': itemData
                    };

                    itemStorage.push(itemData);
                    items.push(readItem);

                    return readItem;
                },

                removeItem = function removeItem (itemIndex) {
                    itemStorage.splice(itemIndex, 1);
                    items.splice(itemIndex, 1);
                },

                removeAllItems = function removeAllItems () {
                    itemStorage.splice(0, itemStorage.length);
                    items.splice(0, items.length);
                },

                getIndexOfItemId = function getIndexOfItemId (itemId) {
                    return _.findIndex(items, function (item) {
                        return item.data.id === itemId;
                    });
                },

                getIndexOfBarcode = function getIndexOfBarcode (barcodeValue) {
                    return _.findIndex(items, function (item) {
                        return item.data.itemId === barcodeValue;
                    });
                },

                getItemById = function getItemById (itemId) {
                    var result = $q.defer();

                    CommonFactory.handlePromise(
                        ItemService.one(itemId).get(),
                        'loadingBarcodesItem',
                        function (item) {
                            result.resolve(item);
                        },
                        function () {
                            result.reject();
                        }
                    );

                    return result.promise;
                };

                fetchItemStorage();

                return {
                    'items': items,
                    'addItem': addItem,
                    'addNewItem': addNewItem,
                    'removeItem': removeItem,
                    'removeAllItems': removeAllItems,
                    'getIndexOfItemId': getIndexOfItemId,
                    'getIndexOfBarcode': getIndexOfBarcode
                };
            },

            /**
             * Class instances
             */
            persistentStorage = persistentStorageClass(),
            itemList = itemListClass(persistentStorage.data.readItems),
            barcodeCache = new BarcodeCacheFactory('loadingBarcodes'),

            /**
             * UI helper functions
             */
            enterNewBarcode = function enterNewBarcode () {
                barcodeCache.getBarcode($scope.newBarcode).then(
                    handleExistingBarcode,
                    handleNewBarcode
                );
                $scope.newBarcode = '';
            },

            handleExistingBarcode = function handleExistingBarcode (barcode) {
                var index = itemList.getIndexOfItemId(barcode.item_id);
                if (index >= 0) {
                    addItemQuantity(index, barcode.quantity);
                } else {
                    itemList.addItem(barcode.item_id, barcode.quantity);
                }
                persistentStorage.save();
            },

            handleNewBarcode = function handleNewBarcode (barcodeValue) {
                var index = itemList.getIndexOfBarcode(barcodeValue);
                if (index >= 0) {
                    addItemQuantity(index, 1);
                } else {
                    itemList.addNewItem(barcodeValue);
                }
                persistentStorage.save();
            },

            addItemQuantity = function addItemQuantity (itemIndex, quantity) {
                if (persistentStorage.data.uiSettings.summarizeMultipleItems) {
                    itemList.items[itemIndex].data.quantity += quantity;
                }
            },

            addNewItem = function addNewItem ($index, readItem) {
            },

            assignToItem = function assignToItem ($index, readItem) {
            },

            printOne = function printOne ($index, readItem) {
            },

            removeItem = function removeItem (itemIndex) {
                var readItem = itemList.items[itemIndex],
                    message;

                if (readItem.id) {
                    message = gettextCatalog.getString(
                        'Do you want to delete item "{{ name }}" ({{ quantity }} {{ unit }})', {
                            'name': readItem.item.name,
                            'quantity': readItem.data.quantity,
                            'unit': readItem.item.unit.unit
                        });
                } else {
                    message = gettextCatalog.getString(
                        'Do you want to delete item "{{ barcode }}" ({{ quantity }})', {
                            'barcode': readItem.data.barcode,
                            'quantity': readItem.data.quantity
                        });
                }

                if ($window.confirm(message)) {
                    itemList.removeItem(itemIndex);
                    persistentStorage.save();
                }
            },

            printAll = function printAll () {
            },

            removeAll = function removeAll () {
                var message = gettextCatalog.getString('Do you want to clear item list?');
                if ($window.confirm(message)) {
                    itemList.removeAllItems();
                    persistentStorage.save();
                }
            },

            addToCurrentView = function addToCurrentView () {
            };


        $scope.readItems = itemList.items;
        $scope.uiSettings = persistentStorage.data.uiSettings;
        $scope.save = persistentStorage.save;

        $scope.newBarcode = '';
        $scope.enterNewBarcode = enterNewBarcode;

        $scope.addNewItem = addNewItem;
        $scope.assignToItem = assignToItem;
        $scope.printOne = printOne;
        $scope.removeItem = removeItem;

        $scope.printAll = printAll;
        $scope.removeAll = removeAll;
        $scope.addToCurrentView = addToCurrentView;
    }]);
