from app.modules.example_data import ExampleAcquisitions as Acquisitions
from test.views.base_api_test import CommonApiTest


class TestAcquisitionWithBrandNewDb(CommonApiTest):
    ENDPOINT = "/acquisitions"

    def test_new_db(self):
        self.assertApiGet(expected_data=[])
        self.assertApiGet(1, expected_status_codes=404)

    def test_adding_new_acquisitions(self):
        self.assertApiPost(data=Acquisitions.ACQUISITION1,
                           expected_data=Acquisitions.ACQUISITION1)
        self.assertApiPost(data=Acquisitions.ACQUISITION2,
                           expected_data=Acquisitions.ACQUISITION2)

    def test_can_add_acquisition_with_same_comment(self):
        self.assertApiPost(data=Acquisitions.ACQUISITION1)
        self.assertApiPost(data=Acquisitions.ACQUISITION2.set(
            change={"comment": Acquisitions.ACQUISITION1["comment"]}))


class TestUserWithPreFilledDb(CommonApiTest):
    ENDPOINT = "/acquisitions"
    INIT_PUSH = [
        (ENDPOINT, [Acquisitions.ACQUISITION1, Acquisitions.ACQUISITION2]),
    ]

    def test_list_acquisitions(self):
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION1,
                                         Acquisitions.ACQUISITION2])

    def test_get_acquisition(self):
        self.assertApiGet(2, expected_data=Acquisitions.ACQUISITION2)
        self.assertApiGet(1, expected_data=Acquisitions.ACQUISITION1)

    def test_remove_acquisition(self):
        self.assertApiDelete(1)
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION2])

    def test_can_not_remove_non_existed_acquisition(self):
        self.assertApiDelete(3, expected_status_codes=404)
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION1,
                                         Acquisitions.ACQUISITION2])

    def test_update_acquisition(self):
        request = Acquisitions.ACQUISITION2.set(change={"comment": "A box has been damaged"})
        response = Acquisitions.ACQUISITION2.get(change={"comment": request["comment"]})

        self.assertApiPut(Acquisitions.ACQUISITION2["id"], data=request, expected_data=response)
        self.assertApiGet(expected_data=[Acquisitions.ACQUISITION1,
                                         response])

    def test_update_name_to_name_of_another_acquisition(self):
        request = Acquisitions.ACQUISITION2.set(change={"comment": Acquisitions.ACQUISITION1["comment"]})

        self.assertApiPut(Acquisitions.ACQUISITION2["id"], data=request)
