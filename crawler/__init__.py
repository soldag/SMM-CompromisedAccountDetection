from .twitter_crawler import crawl_status_updates as crawl_twitter


type_crawler_mapping = {
    'twitter': crawl_twitter
}


def crawl_status_updates(data_source_type, output_path, **kwargs):
    if data_source_type not in type_crawler_mapping:
        raise ValueError('Invalid data_source_type!')

    crawl_callable = type_crawler_mapping[data_source_type]
    return crawl_callable(output_path, **kwargs)

