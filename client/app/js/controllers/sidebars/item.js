'use strict';

var appItemSidebarControllers = angular.module('appControllers.sidebar.item', []);


appItemSidebarControllers.controller('ItemSidebarController', ['$scope',
    function ItemSidebarController ($scope) {
        var readItems = [];

        function addNewBarcode(barcode) {
            console.log(barcode);
            readItems.push({
                'id': 0,
                'name': 'Foo Bar',
                'barcode': barcode
            });
        }

        $scope.readItems = readItems;
        $scope.addNewBarcode = addNewBarcode;
    }]);
