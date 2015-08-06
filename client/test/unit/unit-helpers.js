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
    }
};
