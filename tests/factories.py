# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
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

"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger
from service.models import Promotion,PromoType


class PromotionFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    title = factory.Faker("first_name")
    promo_code = FuzzyChoice(choices=[PromoType.BOGO, PromoType.FIXED, PromoType.DISCOUNT])
    promo_type = FuzzyInteger(1,3)
    amount = FuzzyInteger(1,100)
    start_date = FuzzyDate((date(2008, 1, 1)))
    end_date = FuzzyDate((date(2008, 1, 1)))
    is_site_wide = FuzzyChoice(choices=[True, False])
    product_id = factory.Sequence(lambda n: n)
    #available = FuzzyChoice(choices=[True, False])
    #gender = FuzzyChoice(choices=[Gender.MALE, Gender.FEMALE, Gender.UNKNOWN])
    #birthday = FuzzyDate(date(2008, 1, 1))
    
