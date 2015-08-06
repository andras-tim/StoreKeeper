'use strict';

describe('appSpinner', function () {
    var test;

    beforeEach(module('appDirectives'));

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
                //spyOn(mocks.PageFactory, 'setPageTitle').and.stub();

                inject(function ($compile) {
                    test.$compile = $compile;

                    test.appSpinner = $filter('appSpinner');
                });
            };

        this.mocks = mocks;
        this.injectFilter = injectFilter;
    });

    //it('setTitle() can set the title of page', function () {
    //    test.injectFilter();
    //
    //    expect(test.setTitle('foo')).toEqual('foo');
    //    expect(test.mocks.PageFactory.setPageTitle).toHaveBeenCalledWith('foo');
    //});
});
