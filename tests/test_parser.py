import pytest
import requests

from parspy import get_sp


@pytest.fixture
def url():
    return 'https://freelance.habr.com/tasks'

async def test_get_sp(url):
    """asserts the result of sync and async GETs"""
    sync_get_encdd   = requests.get(url)
    asnc_gt = await get_sp(url)
    # print('status is ', asnc_gt.status)
    # assert sync_get_encdd.status_code == 200
    assert asnc_gt.ok is True
    assert asnc_gt.status == 200

async def test_fails(url):
    asnc_gt = await get_sp(url)
    with pytest.raises(Exception):
        assert asnc_gt.status == 404

    # assert sync_get_encdd == asnc_gt