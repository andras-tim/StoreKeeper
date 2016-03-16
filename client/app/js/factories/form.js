'use strict';

var appFormFactories = angular.module('appFactories.form', []);


appFormFactories.factory('TypeaheadFactory', ['$typeahead', '$parseOptions',
    function TypeaheadFactory ($typeahead, $parseOptions) {
        // based on angular-strap.js

        var defaults = $typeahead.defaults,

            getParsedOptions = function getParsedOptions (config) {
                var filter = config.filter || defaults.filter,
                    limit = config.limit || defaults.limit,
                    comparator = config.comparator || defaults.comparator,
                    bsOptions = config.bsOptions;

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

            createTypeahead = function createTypeahead (scope, element, controller, config) {
                var parsedOptions = getParsedOptions(config),
                    typeahead = $typeahead(element, controller, config),

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
