from app.modules.example_data import ExampleAcquisitions as Acquisitions
from test.views import CommonApiTest


class TestAcquisitionWithBrandNewDb(CommonApiTest):
    def test_new_db(self):
        self.assertRequest("get", "/acquisitions", expected_data=[])
        self.assertRequest("get", "/acquisitions/1", expected_status_codes=404)

    def test_adding_new_acquisitions(self):
        self.assertRequest("post", "/acquisitions", data=Acquisitions.ACQUISITION1.set(),
                           expected_data=Acquisitions.ACQUISITION1.get())
        self.assertRequest("post", "/acquisitions", data=Acquisitions.ACQUISITION2.set(),
                           expected_data=Acquisitions.ACQUISITION2.get())

    def test_can_add_acquisition_with_same_comment(self):
        self.assertRequest("post", "/acquisitions", data=Acquisitions.ACQUISITION1.set())
        self.assertRequest("post", "/acquisitions", data=Acquisitions.ACQUISITION2.set(
            change={"comment": Acquisitions.ACQUISITION1["comment"]}))


class TestUserWithPreFilledDb(CommonApiTest):
    def setUp(self):
        super().setUp()
        self.assertRequest("post", "/acquisitions", data=Acquisitions.ACQUISITION1.set())
        self.assertRequest("post", "/acquisitions", data=Acquisitions.ACQUISITION2.set())

    def test_list_acquisitions(self):
        self.assertRequest("get", "/acquisitions", expected_data=[Acquisitions.ACQUISITION1.get(),
                                                                  Acquisitions.ACQUISITION2.get()])

    def test_get_acquisition(self):
        self.assertRequest("get", "/acquisitions/2", expected_data=Acquisitions.ACQUISITION2.get())
        self.assertRequest("get", "/acquisitions/1", expected_data=Acquisitions.ACQUISITION1.get())

    def test_remove_acquisition(self):
        self.assertRequest("delete", "/acquisitions/1")
        self.assertRequest("get", "/acquisitions", expected_data=[Acquisitions.ACQUISITION2.get()])

    def test_can_not_remove_non_existed_acquisition(self):
        self.assertRequest("delete", "/acquisitions/3", expected_status_codes=404)
        self.assertRequest("get", "/acquisitions", expected_data=[Acquisitions.ACQUISITION1.get(),
                                                                  Acquisitions.ACQUISITION2.get()])

    def test_update_acquisition(self):
        request = Acquisitions.ACQUISITION2.set(change={"comment": "A box has been damaged"})
        response = Acquisitions.ACQUISITION2.get(change={"comment": request["comment"]})

        self.assertRequest("put", "/acquisitions/%d" % Acquisitions.ACQUISITION2["id"], data=request,
                           expected_data=response)
        self.assertRequest("get", "/acquisitions", expected_data=[Acquisitions.ACQUISITION1.get(), response])

    def test_update_name_to_name_of_another_acquisition(self):
        request = Acquisitions.ACQUISITION2.set(change={"comment": Acquisitions.ACQUISITION1["comment"]})

        self.assertRequest("put", "/acquisitions/%d" % Acquisitions.ACQUISITION2["id"], data=request)
