'use strict';

var appBarcodeSidebarControllers = angular.module('appControllers.sidebar.barcode', []);


appBarcodeSidebarControllers.controller('BarcodeSidebarController', ['$scope',
    function BarcodeSidebarController ($scope) {
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
