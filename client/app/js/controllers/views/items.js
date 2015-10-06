'use strict';

var appViewControllers = angular.module('appControllers.views');


appViewControllers.controller('ItemsController', ['$scope', 'ItemService', 'CommonFactory',
    function ItemsController ($scope, ItemService, CommonFactory) {
        function openItem(item) {
            $scope.openModal('item', item.id, item);
        }

        CommonFactory.handlePromise(
            ItemService.getList(),
            'loadingItems',
            function (items) {
                $scope.items = items;
            });

        $scope.openItem = openItem;
    }]);
