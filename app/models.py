from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute

from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection, AllProjection


class User(Model):
    class Meta:
        table_name = "user_results"
        region = "us-east-1"
        host = "http://localhost:8000"
        aws_access_key_id = "cqmfac"
        aws_secret_access_key = "bi1w1"

    search_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    age = NumberAttribute()
    timestamp = NumberAttribute()
    subject = ListAttribute(null=True)


class ViewIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = "timestamp_index"
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    search_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)


class Product(Model):
    class Meta:
        table_name = "product_results"
        region = "us-east-1"
        host = "http://localhost:8000"
        aws_access_key_id = "cqmfac"
        aws_secret_access_key = "bi1w1"

    search_id = UnicodeAttribute(hash_key=True)
    product_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    timestamp = NumberAttribute()
    view_index = ViewIndex()
