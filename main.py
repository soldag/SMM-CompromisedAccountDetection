import argparse

from src import prepare_data
from src import run_pipeline
from src.evaluation import writeToXlsx


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This application analyzes social media posts in order to determine, whether an account was compromised or not.")
    parser.add_argument('--dataset-path', '-p', help='The path of the dataset, which contains the posts.')
    parser.add_argument('--dataset-type', '-t', help='The type of the specified dataset.')
    parser.add_argument('--classifier-type', '-c', help='The type of the classifier to be trained.')
    args = parser.parse_args()

    excel_data = []
    experiment_count = 11
    resources = prepare_data(args.dataset_path, args.dataset_type)

    for i in range(1, experiment_count):
        tp, tn, fp, fn = run_pipeline(resources, args.classifier_type)

        print("Evaluation results:")
        print("True positives: " + str(tp))
        print("True negatives: " + str(tn))
        print("False positives: " + str(fp))
        print("False negatives: " + str(fn))

        excel_data.append([i, tp, tn, fp, fn, (tp + tn)/(tp + tn + fp + fn), tp/(tp + fp), tp/(tp + fn)])

    writeToXlsx(excel_data, experiment_count)
