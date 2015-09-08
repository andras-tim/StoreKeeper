'use strict';

describe('AppTypeahead', function () {
    var test;

    beforeEach(module('appDirectives', 'partials'));

    beforeEach(function () {
        test = this;

        var mocks = {
                'item': {
                    'vendor': {}
                },
                'createVendor': function () {},
                'loadingVendors': undefined,
                'creatingVendor': undefined
            },

            injectDirective = function () {
                spyOn(mocks, 'createVendor').and.stub();

                inject(function ($compile, $rootScope) {
                    test.$compile = $compile;
                    test.$scope = $rootScope.$new();

                    test.$scope.item = mocks.item;
                    test.$scope.createVendor = mocks.createVendor;
                    test.$scope.loadingVendors = mocks.loadingVendors;
                    test.$scope.creatingVendor = mocks.creatingVendor;

                    test.container = helper.compileTemplate(test, '<app-typeahead ' +
                        'app-name="foo" ' +
                        'app-model="item.vendor" ' +
                        'app-label="\'bar\'" ' +
                        'app-data-source="vendor as vendor.name for vendor in $parent.vendors" ' +
                        'app-create-callback="createVendor()" ' +
                        'app-placeholder="\'kakao\'" ' +
                        'app-required="\'Vendor is required\'" ' +
                        'app-loading-spinner="loadingVendors" ' +
                        'app-creating-spinner="creatingVendor"></app-typeahead>');
                });
            };

        this.mocks = mocks;
        this.injectDirective = injectDirective;
    });
    //
    //describe('test isFilled() on model values of input box', function () {
    //
    //    beforeEach(function () {
    //        test.injectDirective();
    //    });
    //
    //    it('string content means it is not filled', function () {
    //        expect(test.$scope.isFilled('')).toBeFalsy();
    //        expect(test.$scope.isFilled('foo')).toBeFalsy();
    //    });
    //
    //    it('dict content means it is filled', function () {
    //        expect(test.$scope.isFilled({})).toBeTruthy();
    //        expect(test.$scope.isFilled({'name': 'foo'})).toBeTruthy();
    //    });
    //});
});
