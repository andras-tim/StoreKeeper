'use strict';

var appViewControllers = angular.module('appControllers.views');


appViewControllers.controller('ItemsController', ['$scope', '$location', '$modal', 'ItemService', 'CommonFactory',
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
