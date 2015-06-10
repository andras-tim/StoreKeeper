'use strict';

describe('service', function () {

    beforeEach(module('storekeeperApp'));

    it('check the existence of factory of services ', inject(function (SessionService, ConfigService) {
        expect(SessionService).toBeDefined();
        expect(ConfigService).toBeDefined();
    }));

});
