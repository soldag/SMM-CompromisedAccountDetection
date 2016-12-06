import argparse

from core import prepare_data
from core import run_pipeline
from core.evaluation import writeToXlsx

from crawler import crawl_status_updates


def analyze(data_source_type, classifier_type, experiments_count,
            dataset_path=None, twitter_user=None):
    # Get status updates and prepare data
    print("Retrieve and prepare data...")
    provider_parameter = {}
    if dataset_path is not None:
        provider_parameter["dataset_path"] = dataset_path
    elif data_source_type == "twitter" and twitter_user is not None:
        provider_parameter["user_id"] = twitter_user
    else:
        raise ValueError("Either dataset_path or twitter_user has to be provided.")
    status_updates = prepare_data(data_source_type, **provider_parameter)

    # Run specified number of experiments
    evaluation_data = []
    for i in range(0, experiments_count):
        tp, tn, fp, fn = run_pipeline(status_updates, classifier_type)
        evaluation_data.append([i, tp, tn, fp, fn, (tp + tn) / (tp + tn + fp + fn), tp / (tp + fp), tp / (tp + fn)])

        print("Evaluation results for experiment %i/%i" % (i + 1, experiments_count))
        print("True positives: " + str(tp))
        print("True negatives: " + str(tn))
        print("False positives: " + str(fp))
        print("False negatives: " + str(fn))

    writeToXlsx(evaluation_data, experiments_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This application analyzes social media status updates in order to determine, whether an account was compromised or not.")
    parser.add_argument("--action", "-a",
                        help="The action that should be performed. Possible values are 'crawl' and 'analyze'.")
    parser.add_argument("--data-source-type", "-t", default=None,
                        help="The type of the specified data source. Possible values are 'fth', 'mp' and 'twitter'.")

    # Data source arguments
    parser.add_argument("--dataset-path", "-p", default=None,
                        help="The path of the dataset, which contains the status_updates. ")
    parser.add_argument("--twitter-user", "-u", default=None,
                        help="The id of the twitter user, whose status updates should be analyzed.")

    # Crawl arguments
    parser.add_argument("--user-limit", type=int, default=100,
                        help="The maximum number of accounts to crawl.")

    # Train arguments
    parser.add_argument("--classifier-type", "-c", default=None,
                        help="The type of the classifier to be trained. ")
    parser.add_argument("--experiments-count", "-n", type=int, default=10,
                        help="The number of experiments to run.")

    args = parser.parse_args()

    if args.action == 'crawl':
        crawl_status_updates(args.data_source_type, args.dataset_path,
                             user_limit=args.user_limit)
    elif args.action == 'analyze':
        analyze(args.data_source_type, args.classifier_type,
                args.experiments_count, args.dataset_path, args.twitter_user)
    else:
        print("Invalid mode!")
