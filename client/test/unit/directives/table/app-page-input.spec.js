'use strict';

describe('Directives/Table: appPageInput', function () {
    var test;

    beforeEach(module('appDirectives.table', 'partials'));

    beforeEach(function () {
        test = this;

        var mocks = {
                'selectPage': function () {}
            },

            injectDirective = function () {
                spyOn(mocks, 'selectPage').and.stub();

                inject(function ($compile, $rootScope) {
                    test.$compile = $compile;
                    test.$scope = $rootScope.$new();

                    test.$scope.selectPage = mocks.selectPage;

                    test.container = helper.compileTemplate(test, '<app-page-input />');
                });
            };

        this.mocks = mocks;
        this.injectDirective = injectDirective;
    });

    it('input box have to always contain the number of current page', function () {
        test.injectDirective();

        expect(test.container.find('input').length).toBe(1);
        expect(test.container.find('input').val()).toEqual('');

        test.$scope.currentPage = 1;
        test.$scope.$apply();
        expect(test.container.find('input').val()).toEqual('1');

        test.$scope.currentPage = 42;
        test.$scope.$apply();
        expect(test.container.find('input').val()).toEqual('42');
    });

    it('input change have to synced to current page', function () {
        test.injectDirective();

        expect(test.container.find('input').length).toBe(1);
        expect(test.mocks.selectPage).not.toHaveBeenCalled();

        test.container.find('input').val('1');
        test.container.find('input').triggerHandler('change');
        expect(test.mocks.selectPage).toHaveBeenCalledWith('1');

        test.container.find('input').val('42');
        test.container.find('input').triggerHandler('change');
        expect(test.mocks.selectPage).toHaveBeenCalledWith('42');
    });

});
