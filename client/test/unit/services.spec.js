'use strict';

describe('Services', function () {
    beforeEach(function () {
        module('storekeeperApp');
    });

    it('check the existence of factory of factories ', inject(function (SessionService, ConfigService) {
        expect(SessionService).toBeDefined();
        expect(ConfigService).toBeDefined();
    }));

});
