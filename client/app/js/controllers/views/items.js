'use strict';

var appViewControllers = angular.module('appControllers.views');


appViewControllers.controller('ItemsController', ['$rootScope', '$scope', '$window', 'ItemService', 'CommonFactory',
    function ItemsController ($rootScope, $scope, $window, ItemService, CommonFactory) {
        var updateItemsDestroyer,
            updateTimer;

        function openItem(item) {
            $scope.openModal('item', item.id, item);
        }

        function updateItems() {
            CommonFactory.handlePromise(
                ItemService.getList(),
                'loadingItems',
                function (items) {
                    $scope.items = items;
                });
        }

        function periodicallyUpdateItems() {
            updateItems();
            updateTimer = $window.setTimeout(periodicallyUpdateItems, 300000); // 5 min
        }

        updateItemsDestroyer = $rootScope.$on('updateItems', updateItems);
        $scope.$on('$destroy', function destructItemsController () {
            $window.clearTimeout(updateTimer);
            updateItemsDestroyer();
        });

        periodicallyUpdateItems();

        $scope.openItem = openItem;
    }]);
