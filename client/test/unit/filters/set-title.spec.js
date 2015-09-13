'use strict';

describe('Filters: setTitleFilter', function () {
    var test;

    beforeEach(module('appFilters'));

    beforeEach(function () {
        test = this;

        var mocks = {
                'PageFactory': {
                    'setPageTitle': function () {}
                }
            },

            injectFilter = function () {
                module(function ($provide) {
                    $provide.value('PageFactory', mocks.PageFactory);
                });
                spyOn(mocks.PageFactory, 'setPageTitle').and.stub();

                inject(function ($filter) {
                    test.setTitle = $filter('setTitle');
                });
            };

        this.mocks = mocks;
        this.injectFilter = injectFilter;
    });

    it('setTitle() can set the title of page', function () {
        test.injectFilter();

        expect(test.setTitle('foo')).toEqual('foo');
        expect(test.mocks.PageFactory.setPageTitle).toHaveBeenCalledWith('foo');
    });
});
