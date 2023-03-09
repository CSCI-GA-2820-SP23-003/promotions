"""
Test Factory to make fake objects for testing
"""
from datetime import datetime, timedelta, timezone
import string
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyText, FuzzyInteger
from service.models import Promotion, PromoType

JST = timezone(timedelta(hours=+9))


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
    start_date = FuzzyDateTime(
        datetime(2023, 1, 1).replace(tzinfo=timezone.utc),
        datetime(2023, 12, 31).replace(tzinfo=timezone.utc)
        )
    end_date = FuzzyDateTime(
        datetime(2024, 1, 1).replace(tzinfo=timezone.utc),
        datetime(2024, 12, 31).replace(tzinfo=timezone.utc)
        )
    is_site_wide = FuzzyChoice(choices=[True, False])
    product_id = FuzzyInteger(1, 100)
