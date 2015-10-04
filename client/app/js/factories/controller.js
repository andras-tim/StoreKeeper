'use strict';

var appControllerFactories = angular.module('appFactories.controller', []);


appControllerFactories.factory('TypeaheadFactory', ['$typeahead', '$parseOptions',
    function TypeaheadFactory ($typeahead, $parseOptions) {
        // based on angular-strap.js

        var defaults = $typeahead.defaults,

            getParsedOptions = function getParsedOptions (options) {
                var filter = options.filter || defaults.filter,
                    limit = options.limit || defaults.limit,
                    comparator = options.comparator || defaults.comparator,
                    bsOptions = options.bsOptions;

                if (filter) {
                    bsOptions += ' | ' + filter + ':$viewValue';
                }
                if (comparator) {
                    bsOptions += ':' + comparator;
                }
                if (limit) {
                    bsOptions += ' | limitTo:' + limit;
                }

                return $parseOptions(bsOptions);
            },

            createTypeahead = function createTypeahead (scope, element, controller, options) {
                var parsedOptions = getParsedOptions(options),
                    typeahead = $typeahead(element, controller, options),

                    updateTypeahead = function updateTypeahead () {
                        parsedOptions.valuesFn(scope, controller).then(function (values) {
                            typeahead.update(values);
                            controller.$render();
                        });
                    };

                return {
                    'object': typeahead,
                    'update': updateTypeahead
                };
            };

        return {
            'createTypeahead': createTypeahead
        };
    }]);
