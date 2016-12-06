import argparse

from core import prepare_data
from core import run_pipeline
from core.evaluation import writeToXlsx


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This application analyzes social media status updates in order to determine, whether an account was compromised or not.")
    parser.add_argument("--provider-type", "-t", help="The type of the specified data provider.")
    parser.add_argument("--classifier-type", "-c", help="The type of the classifier to be trained.")
    parser.add_argument("--experiments-count", "-n", default=10, help="The number of experiments to run.")
    parser.add_argument("--dataset-path", default=None, help="The path of the dataset, which contains the status_updates. (only required, if 'fth' or 'mp 'is used as data provider)")
    parser.add_argument("--twitter-user", default=None, help="The id of the twitter user, whose status updates should be analyzed. (only required, if 'twitter' is used as data provider)")
    args = parser.parse_args()

    # Get status updates and prepare data
    print("Retrieve and prepare data...")
    provider_parameter = {}
    if args.dataset_path is not None:
        provider_parameter["dataset_path"] = args.dataset_path
    if args.twitter_user is not None:
        provider_parameter["user_id"] = args.twitter_user
    status_updates = prepare_data(args.provider_type, **provider_parameter)

    # Run specified number of experiments
    evaluation_data = []
    experiments_count = int(args.experiments_count)
    for i in range(0, experiments_count):
        tp, tn, fp, fn = run_pipeline(status_updates, args.classifier_type)
        evaluation_data.append([i, tp, tn, fp, fn, (tp + tn) / (tp + tn + fp + fn), tp / (tp + fp), tp / (tp + fn)])

        print("Evaluation results for experiment %i/%i" % (i + 1, experiments_count))
        print("True positives: " + str(tp))
        print("True negatives: " + str(tn))
        print("False positives: " + str(fp))
        print("False negatives: " + str(fn))

    writeToXlsx(evaluation_data, experiments_count)
