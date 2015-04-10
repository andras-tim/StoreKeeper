from app.modules.example_data import ExampleUnits as Units
from test.views.base_api_test import CommonApiTest, append_mandatory_field_tests


@append_mandatory_field_tests(item_name='unit', base_item=Units.UNIT1,
                              mandatory_fields=['unit'])
class TestUnitWithBrandNewDb(CommonApiTest):
    ENDPOINT = '/units'

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_units(self):
        self.assertApiPost(data=Units.UNIT1, expected_data=Units.UNIT1)
        self.assertApiPost(data=Units.UNIT2, expected_data=Units.UNIT2)

    def test_can_not_add_unit_with_same_name(self):
        self.assertApiPost(data=Units.UNIT1)
        self.assertApiPost(data=Units.UNIT2.set(change={'unit': Units.UNIT1['unit']}),
                           expected_data={'message': {'unit': ['Already exists.']}},
                           expected_status_codes=422)


class TestUnitWithPreFilledDb(CommonApiTest):
    ENDPOINT = '/units'
    INIT_PUSH = [
        (ENDPOINT, [Units.UNIT1, Units.UNIT2]),
    ]

    def test_list_units(self):
        self.assertApiGet(expected_data=[Units.UNIT1,
                                         Units.UNIT2])

    def test_get_unit(self):
        self.assertApiGet(2, expected_data=Units.UNIT2)
        self.assertApiGet(1, expected_data=Units.UNIT1)

    def test_remove_unit(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Units.UNIT2])

    def test_can_not_remove_non_existed_unit(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Units.UNIT1,
                                         Units.UNIT2])

    def test_update_unit(self):
        request = Units.UNIT2.set(change={'unit': 'foo2'})
        response = Units.UNIT2.get(change={'unit': request['unit']})

        self.assertApiPut(Units.UNIT2['id'], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Units.UNIT1,
                                         response])

    def test_update_name_to_name_of_another_unit(self):
        request = Units.UNIT2.set(change={'unit': Units.UNIT1['unit']})

        self.assertApiPut(Units.UNIT2['id'], data=request, expected_status_codes=422)
