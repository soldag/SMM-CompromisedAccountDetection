from .fth_parser import parse_dataset as parse_fth


type_parser_mapping = {
    'fth': parse_fth
}


def parse_dataset(path, dataset_type):
    if dataset_type not in type_parser_mapping:
        raise ValueError('Invalid dataset_type!')

    parsing_callable = type_parser_mapping[dataset_type]
    return parsing_callable(path)

