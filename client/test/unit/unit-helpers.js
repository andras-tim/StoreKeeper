'use strict';

/*jshint -W098 */ //Disable warning for variable never used
var helper = {
    'promiseMock': function promiseMock (test, conditionVariableInTest, resolvedValue, rejectedValue) {
        var deferred = test.$q.defer();

        if (test[conditionVariableInTest]) {
            deferred.resolve(resolvedValue);
        } else {
            deferred.reject(rejectedValue);
        }

        return deferred.promise;
    },

    'compileTemplate': function compileTemplate (test, htmlTemplate, $scope) {
        if ($scope === undefined) {
            $scope = test.$scope;
        }

        var compiledHtml = test.$compile(angular.element(htmlTemplate))(test.$scope);
        $scope.$apply();

        return compiledHtml;
    }
};
