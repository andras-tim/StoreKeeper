'use strict';

describe('appSpinner', function () {
    var test;

    beforeEach(module('appDirectives', 'partials'));

    beforeEach(function () {
        test = this;

        var injectDirective = function () {
                inject(function ($compile, $rootScope) {
                    test.$compile = $compile;
                    test.$scope = $rootScope.$new();

                    test.container = helper.compileTemplate(test, '<span app-spinner="fooSpinner" />');
                });
            };

        this.injectDirective = injectDirective;
    });

    it('show spinner only when spinning is true', function () {
        test.injectDirective();

        expect(test.container.find('.fa-spinner').length).toBe(0);

        test.$scope.fooSpinner = false;
        test.$scope.$apply();
        expect(test.container.find('.fa-spinner').length).toBe(0);

        test.$scope.fooSpinner = true;
        test.$scope.$apply();
        expect(test.container.find('.fa-spinner').length).toBe(1);
    });
});
