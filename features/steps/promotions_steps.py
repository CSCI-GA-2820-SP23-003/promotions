######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Promotions Steps

Steps file for Promotions.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

import requests
import behave
from compare import expect


@behave.given('the following promotions')
def step_impl(context):
    """ Start Server and delete and load new ones """
    # List all of the promotions and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/promotions"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for promotion in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{promotion['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new promotions
    for row in context.table:
        payload = {
            "title": row["Title"],
            "promo_code": row["Code"],
            "promo_type": row["Type"],
            "amount": row["Amount"],
            "start_date": row["Start"],
            "end_date": row["End"],
            "is_site_wide": row["Is_Site_Wide"] in ['True','true','1'],
            "product_id": row["ProductID"]
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)