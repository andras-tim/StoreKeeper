'use strict';

var appSidebarControllers = angular.module('appControllers.sidebars');


appSidebarControllers.controller('ItemSidebarController', ['$scope', '$q', '$log', '$window', 'gettextCatalog', 'Restangular', 'CommonFactory', 'BarcodeCacheFactory', 'ItemCacheFactory', 'PersistFactory', 'StocktakingService',
    function ItemSidebarController ($scope, $q, $log, $window, gettextCatalog, Restangular, CommonFactory, BarcodeCacheFactory, ItemCacheFactory, PersistFactory, StocktakingService) {
        var
            /**
             * Persistent storage
             *
             * It can load and save settings of this controller
             */
            persistentStorageClass = function persistentStorageClass () {
                var storage = PersistFactory.load('sidebar_item', 1),
                    data = storage.data;

                if (!data.readElements) {
                    data.readElements = [];
                }

                if (!data.uiSettings) {
                    data.uiSettings = {};
                }

                return {
                    'data': data,
                    'save': storage.save
                };
            },

            /**
             * Persistable element storage
             *
             * Element structure:
             * {
             *   'item': <Item by ItemService>,
             *   'data': <reference of persisted 'barcode', 'barcodeQuantity', 'itemId', 'count' contained object>
             * }
             */
            readElementsClass = function readElementsClass (elementStorage, barcodeCache, itemCache) {
                var elements = [],
                    initialized = false,

                fetchItemStorage = function fetchItemStorage () {
                    var length = elementStorage.data.readElements.length,
                        index,
                        element;

                    for (index = 0; index < length; index += 1) {
                        element = elementStorage.data.readElements.shift();
                        addElement(element.barcode, element.count);
                    }

                    initialized = true;
                },

                addElement = function addElement (barcodeValue, count) {
                    barcodeCache.getBarcode(barcodeValue).then(
                        function (barcode) {
                            addExistingElement(barcode, count);
                        }, function (barcodeValue) {
                            addNewElement(barcodeValue, count);
                        }
                    );
                },

                addExistingElement = function addExistingElement (barcode, count) {
                    var element = pushElementData({
                            'barcode': barcode.barcode,
                            'itemId': barcode.item_id,
                            'count': count || 1
                        });

                    element.barcode = barcode;
                    itemCache.getItemById(barcode.item_id).then(function (item) {
                        element.item = item;
                    });
                },

                addNewElement = function createNewElement (barcodeValue, count) {
                    pushElementData({
                        'barcode': barcodeValue,
                        'itemId': null,
                        'count': count || 1
                    });
                },

                pushElementData = function pushElementData (elementData) {
                    var element = {
                        'barcode': null,
                        'item': null,
                        'data': elementData
                    };

                    elementStorage.data.readElements.push(elementData);
                    elements.push(element);

                    onElementChange();
                    return element;
                },

                removeElement = function removeElement (elementIndex) {
                    elementStorage.data.readElements.splice(elementIndex, 1);
                    elements.splice(elementIndex, 1);
                    onElementChange();
                },

                removeAllElements = function removeAllElements () {
                    elementStorage.data.readElements.splice(0, elementStorage.data.readElements.length);
                    elements.splice(0, elements.length);
                    onElementChange();
                },

                getIndexByBarcode = function getIndexByBarcode (barcode) {
                    return _.findIndex(elements, function (element) {
                        return element.data.barcode === barcode;
                    });
                },

                onElementChange = function onElementChange () {
                    saveChanges();
                    checkAllElementsHasBeenAssigned();
                },

                saveChanges = function saveChanges () {
                    if (initialized) {
                        elementStorage.save();
                    }
                },

                checkAllElementsHasBeenAssigned = function checkAllElementsHasBeenAssigned () {
                    if (!initialized) {
                        return;
                    }

                    var length = elements.length,
                        index,
                        element;

                    for (index = 0; index < length; index += 1) {
                        element = elements[index];
                        if (!element.data.itemId) {
                            $scope.movable = false;
                            return;
                        }
                        $scope.movable = true;
                    }
                };

                fetchItemStorage();
                checkAllElementsHasBeenAssigned();

                return {
                    'elements': elements,
                    'addElement': addElement,
                    'removeElement': removeElement,
                    'removeAllElements': removeAllElements,
                    'getIndexByBarcode': getIndexByBarcode
                };
            },

            /**
             * Class instances
             */
            barcodeCache = new BarcodeCacheFactory('itemSidebarLoadingBarcodes'),
            itemCache = new ItemCacheFactory('itemSidebarLoadingBarcodeItem'),
            persistentStorage = persistentStorageClass(),
            readElements = readElementsClass(persistentStorage, barcodeCache, itemCache),

            /**
             * UI helper functions
             */
            enterElement = function enterElement () {
                var barcode;

                if (angular.isObject($scope.searchField)) {
                    barcode = getBarcodeFromObject($scope.searchField);
                } else {
                    barcode = normalizeReadData($scope.searchField);
                }

                addElement(barcode);
                $scope.searchField = '';
            },

            normalizeReadData = function normalizeReadData (data) {
                var unLocalizedData,
                    translate = {
                        //'!': '$', // FIXME: can not detect keyboard layout in JS
                        //'-': '/', // FIXME: translated only the unequivocal translatable symbols from Code39 and 93 standards
                        'ö': '0',
                        'ü': '-',
                        'Ó': '+',
                        '(': '*'
                    },
                    translateRe = /[öüÓ(]/g;

                unLocalizedData = (data.replace(translateRe, function (match) {
                    return translate[match];
                }));

                return unLocalizedData.toUpperCase();
            },

            addElement = function addElement (barcodeValue) {
                var index = readElements.getIndexByBarcode(barcodeValue);

                if (index >= 0) {
                    readElements.elements[index].data.count += 1;
                    persistentStorage.save();
                } else {
                    readElements.addElement(barcodeValue);
                }
            },

            createNewElement = function createNewElement (readElement, barcodeValue) {
                var elementData = {
                    'new': {},

                    'onSave': function onSave (item, barcodes) {
                        if (angular.isUndefined(readElement) && barcodes.length) {
                            barcodeCache.refresh().then(function () {
                                addElement(barcodes[0].barcode);
                            });
                        } else {
                            readElement.data.itemId = item.id;
                            readElement.item = item;
                            readElement.barcode = barcodes[0];
                        }
                        $scope.closeModal('item');
                    }
                };

                if (angular.isDefined(barcodeValue)) {
                    elementData.new.barcode = barcodeValue;
                }

                $scope.openModal('item', 0, elementData);
            },

            getBarcodeFromObject = function getBarcodeFromObject (selectedObject) {
                if (selectedObject.type === 'barcode') {
                    return selectedObject.barcode;
                } else if (selectedObject.type === 'item') {
                    return selectedObject.master_barcode;
                }
                $log.error('Unknown object type', selectedObject.type);
            },

            addBarcodeToANewItem = function addBarcodeToANewItem ($index, readElement) {
                createNewElement(readElement, readElement.data.barcode);
            },

            assignBarcodeToAnExistingItem = function assignBarcodeToAnExistingItem ($index, readElement) {
                var elementData = {
                    'defaultButtonTitle': gettextCatalog.getString('Assign to item'),
                    'selectedItem': '',
                    'barcodeQuantity': 1,

                    'onItemSelect': function onItemSelect () {
                        addBarcodeToItem(elementData.selectedItem.item_id, readElement.data.barcode, elementData.barcodeQuantity, readElement).then(
                            function () {
                                $scope.closeModal('item-selector');
                            });
                    }
                };

                $scope.openModal('item-selector', null, elementData);
            },

            addBarcodeToItem = function addBarcodeToItem (itemId, barcodeValue, barcodeQuantity, localElement) {
                function updateLocalState(barcodeObject) {
                    localElement.data.itemId = itemId;
                    persistentStorage.save();

                    localElement.barcode = barcodeObject;
                    itemCache.getItemById(itemId).then(function (item) {
                        localElement.item = item;
                        return $q.when();
                    }).then(function () {
                        return barcodeCache.refresh();
                    });
                }

                return itemCache.getItemById(itemId).then(function (item) {
                    var barcode = {
                        'barcode': barcodeValue,
                        'quantity': barcodeQuantity
                    };

                    return CommonFactory.handlePromise(
                        item.all('barcodes').post(Restangular.copy(barcode)),
                        'itemSelectorOperation',
                        updateLocalState);
                });
            },

            printElement = function printElement ($index, readElement) {
                itemCache.getItemById(readElement.data.itemId).then(
                    function (item) {
                        CommonFactory.handlePromise(
                            item.one('barcodes', readElement.barcode.id).customPUT(null, 'print'),
                            'itemSidebarPrintingLabel'
                        );
                    });
            },

            removeElement = function removeElement (elementIndex) {
                var readElement = readElements.elements[elementIndex],
                    message;

                if (readElement.data.itemId) {
                    message = gettextCatalog.getString(
                        'Do you want to delete element "{{ barcode }}" ({{ count }} x {{ quantity }} {{ unit }} of item "{{ name }}")', {
                            'barcode': readElement.data.barcode,
                            'count': readElement.data.count,
                            'quantity': readElement.data.quantity,
                            'unit': readElement.item.unit.unit,
                            'name': readElement.item.name
                        });
                } else {
                    message = gettextCatalog.getString(
                        'Do you want to delete element "{{ barcode }}" ({{ count }} pcs)', {
                            'barcode': readElement.data.barcode,
                            'count': readElement.data.count
                        });
                }

                if ($window.confirm(message)) {
                    readElements.removeElement(elementIndex);
                }
            },

            showElement = function showElement ($index, readElement) {
                $scope.openModal('item', readElement.item.id, readElement.item);
            },

            printAllElements = function printAllElements () {
                var count = getCountOfPrintableLabels(),
                    message = gettextCatalog.getString('Do you want to print sum {{ count }} pcs. labels?', {
                        'count': count
                    });

                if (!$window.confirm(message)) {
                    return;
                }

                _.forEach(readElements.elements, function (readElement) {
                    if (!readElement.barcode) {
                        return;
                    }
                    itemCache.getItemById(readElement.data.itemId).then(
                        function (item) {
                            CommonFactory.handlePromise(
                                item.one('barcodes', readElement.barcode.id).customPUT({'copies': Math.abs(readElement.data.count)}, 'print'),
                                'itemSidebarPrintingLabel'
                            );
                        });
                });
            },

            getCountOfPrintableLabels = function getCountOfPrintableLabels () {
                var length = readElements.elements.length,
                    readElement,
                    index,
                    count = 0;

                for (index = 0; index < length; index += 1) {
                    readElement = readElements.elements[index];
                    if (readElement.barcode) {
                        count += Math.abs(readElement.data.count);
                    }
                }

                return count;
            },

            removeAllElements = function removeAllElements () {
                var message = gettextCatalog.getString('Do you want to clear list?');
                if ($window.confirm(message)) {
                    readElements.removeAllElements();
                }
            },

            moveElementsToCurrentView = function moveElementsToCurrentView () {
                var message,
                    mergedElements,
                    elementPromises;

                message = gettextCatalog.getString('Do you want to move all element from list to Items?');
                if (!$window.confirm(message)) {
                    return;
                }

                mergedElements = getMergedElementsByItem();
                elementPromises = [];

                CommonFactory.handlePromise(
                    StocktakingService.post({
                        'comment': '[initial input]'
                    }),
                    'itemSidebarMovingItems'
                ).then(function (stocktaking) {
                    var itemId,
                        element;

                    for (itemId in mergedElements) {
                        if (mergedElements.hasOwnProperty(itemId)) {
                            element = mergedElements[itemId];

                            elementPromises.push(
                                CommonFactory.handlePromise(
                                    stocktaking.all('items').post({
                                        'item': element.item,
                                        'quantity': element.quantity
                                    }),
                                    'itemSidebarMovingItems')
                            );
                        }
                    }

                    $q.all(elementPromises).then(function () {
                        CommonFactory.handlePromise(
                            stocktaking.customPUT(null, 'close'),
                            'itemSidebarMovingItems',
                            function () {
                                readElements.removeAllElements();
                            }
                        );
                    });
                });
            },

            getMergedElementsByItem = function getMergedElementsByItem () {
                var items = {},
                    length = readElements.elements.length,
                    index,
                    element,
                    itemId;

                for (index = 0; index < length; index += 1) {
                    element = readElements.elements[index];
                    itemId = element.data.itemId;

                    if (angular.isUndefined(items[itemId])) {
                        items[itemId] = {
                            'item': element.item,
                            'quantity': element.barcode.quantity * element.data.count
                        };
                    } else {
                        items[itemId].quantity += element.barcode.quantity * element.data.count;
                    }
                }

                return items;
            };


        $scope.readElements = readElements.elements;
        $scope.uiSettings = persistentStorage.data.uiSettings;
        $scope.save = persistentStorage.save;

        $scope.searchField = '';
        $scope.enterElement = enterElement;
        $scope.createNewElement = createNewElement;

        $scope.addBarcodeToANewItem = addBarcodeToANewItem;
        $scope.assignBarcodeToAnExistingItem = assignBarcodeToAnExistingItem;
        $scope.printElement = printElement;
        $scope.removeElement = removeElement;
        $scope.showElement = showElement;

        $scope.printAllElements = printAllElements;
        $scope.removeAllElements = removeAllElements;
        $scope.moveElementsToCurrentView = moveElementsToCurrentView;
    }]);
