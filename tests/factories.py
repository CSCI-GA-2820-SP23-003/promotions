"""
Test Factory to make fake objects for testing
"""
from datetime import date
import string

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyText, FuzzyInteger
from service.models import Promotion, PromoType


class PromotionsFactory(factory.Factory):
    """Creates fake promotions that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    title = FuzzyText(length=12, chars=string.ascii_letters, prefix='promo_')
    promo_code = FuzzyText(length=5, chars=string.ascii_letters, prefix='')
    promo_type = FuzzyChoice(choices=[PromoType.BOGO, PromoType.DISCOUNT, PromoType.FIXED])
    amount = FuzzyInteger(10, 100)
    start_date = FuzzyDate(date(2023, 1, 1), date(2023, 12, 31))
    end_date = FuzzyDate(date(2024, 1, 1), date(2024, 12, 31))
    is_site_wide = FuzzyChoice(choices=[True, False])
    product_id = FuzzyInteger(1, 100)
