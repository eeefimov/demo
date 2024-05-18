"""Params for ingredients api"""
import pytest
from faker import Faker

fake = Faker()

# ingredients invalid methods:
invalid_methods = [
    pytest.param('post',
                 404,
                 id='POST'),
    pytest.param('put',
                 404,
                 id='PUT'),
    pytest.param('patch',
                 404,
                 id='PATCH')
]

# headers validation
header_validation = [
    pytest.param({'Content-Type': 'application/json; charset=utf-8'},
                 200,
                 id='application/json; charset=utf-8'),
    pytest.param({'Content-Type': None},
                 200,
                 id='None'),
    pytest.param({'Content-Type': 'Application/Json'},
                 200,
                 id='Application/Json'),
    pytest.param({'Content-Type': 'APPLICATION/JSON'},
                 200,
                 id='APPLICATION/JSON'),
    pytest.param({'Content-Type': 'APPLICATION/'},
                 200,
                 id='APPLICATION/'),
    pytest.param({'Content-Type': 'application/text'},
                 200,
                 id='application/text'),
    pytest.param({'Content-Type': 'application/html'},
                 200,
                 id='application/html'),
    pytest.param({'Content-Type': 'application/json',
                  'Authorization': ''},
                 200,
                 id='Authorization ""'),
    pytest.param({'Content-Type': 'application/json',
                  'Authorization': 'empty'},
                 200,
                 id='Authorization: valid token'),
    pytest.param({'Content-Type': 'application/xml'},
                 200,
                 id='application/xml'),
]
