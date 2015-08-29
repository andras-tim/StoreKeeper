'use strict';

var appFilters = angular.module('appFilters', []);


appFilters.filter('setTitle', ['PageFactory',
    function setTitle (PageFactory) {
        return function (title) {
            PageFactory.setPageTitle(title);
            return title;
        };
    }]);


appFilters.filter('isContainedInNested', ['$parse', '$filter',
    function isContainedInNested ($parse, $filter) {
        function filterInAllFields(items, filters) {
            var filter = $filter('filter');
            return filter(items, {'$': filters.$});
        }

        function filter(items, filters) {
            var itemsLeft;
            if ('$' in filters) {
                itemsLeft = filterInAllFields(items, filters);
            } else {
                itemsLeft = items.slice();
            }

            Object.keys(filters).forEach(function (model) {
                if (model === '$') {
                    return false;
                }

                var expected = filters[model].name.toLowerCase(),
                    getter = $parse(model);

                itemsLeft = itemsLeft.filter(function (item) {
                    var actual = getter(item);
                    return actual.name.toLowerCase().indexOf(expected) !== -1;
                });
            });

            return itemsLeft;
        }

        return filter;
    }]);
