import uuid

import pytest

from job_posts_models import HabrWorkHeader


class TestWorkHeaders:
    # container = [HabrWorkHeader(
    #     uuid.uuid4(),
    #     'Make a test',
    #     price='10000',
    #     util_info='day ago',
    #     source='habr',
    #     tags=['python', 'devops']
    # )]

    @pytest.fixture
    def header0(self):
        test_header = HabrWorkHeader(
            uuid.uuid4(),
            'Make a test',
            price='10000',
            util_info='day ago',
            source='habr',
            tags=['python', 'devops']
        )
        return test_header

    @pytest.fixture
    def header1(self):
        test_header = HabrWorkHeader(
            uuid.uuid4(),
            'Make a test',
            price='10000',
            util_info='2 days ago',
            source='habr',
            tags=['python', 'devops']
        )
        return test_header

    @pytest.fixture
    def container(self, header0):
        return [header0]

    # @pytest.mark.xfail
    def test_in_on_eq_and_not_same(self, header1, container):
        assert header1 in container

    def test_in_on_similarity(self, header0, container):
        assert header0 in container

    def test_equality(self, header0, header1):
        assert header0 == header1
