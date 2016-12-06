from .fth_provider import FthProvider
from .mp_provider import MpProvider
from .twitter_provider import TwitterProvider


type_provider_mapping = {
    'fth': FthProvider,
    'mp': MpProvider,
    'twitter': TwitterProvider
}


def get_status_updates(data_source_type, **kwargs):
    if data_source_type not in type_provider_mapping:
        raise ValueError('Invalid data_source_type!')

    provider = type_provider_mapping[data_source_type]()
    return provider.get_status_updates(**kwargs)

