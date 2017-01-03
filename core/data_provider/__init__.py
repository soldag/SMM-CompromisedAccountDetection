from .fth_provider import FthProvider
from .mp_provider import MpProvider
from .twitter_provider import TwitterProvider


TYPE_PROVIDER_MAPPING = {
    'fth': FthProvider,
    'mp': MpProvider,
    'twitter': TwitterProvider
}


def get_status_updates(data_source_type, **kwargs):
    if data_source_type not in TYPE_PROVIDER_MAPPING:
        raise ValueError('Invalid data_source_type!')

    provider = TYPE_PROVIDER_MAPPING[data_source_type]()
    return sorted(provider.get_status_updates(**kwargs),
                  key=lambda x: x.date_time)

