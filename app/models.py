from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute


class User(Model):
    class Meta:
        table_name = "user_results"
        region = "us-east-1"
        host = 'http://localhost:8000'
        aws_access_key_id = 'cqmfac'
        aws_secret_access_key = 'bi1w1'
    search_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    age = NumberAttribute()
    timestamp = NumberAttribute()
    subject = ListAttribute(null=True)
