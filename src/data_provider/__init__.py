from .fth_provider import get_status_updates as get_fth
from .mp_provider import get_status_updates as get_mp
from .twitter_provider import get_status_updates as get_twitter


type_provider_mapping = {
    'fth': get_fth,
    'mp': get_mp,
    'twitter': get_twitter
}


def get_status_updates(provider_type, **kwargs):
    if provider_type not in type_provider_mapping:
        raise ValueError('Invalid provider_type!')

    parsing_callable = type_provider_mapping[provider_type]
    return parsing_callable(**kwargs)

