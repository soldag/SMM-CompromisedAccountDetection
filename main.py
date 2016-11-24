import argparse

from src import run_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This application analyzes social media posts in order to determine, whether an account was compromised or not.")
    parser.add_argument('--dataset-path', '-p', help='The path of the dataset, which contains the posts.')
    parser.add_argument('--dataset-type', '-t', help='The type of the specified dataset.')
    parser.add_argument('--classifier-type', '-c', help='The type of the classifier to be trained.')
    args = parser.parse_args()

    tp, tn, fp, fn = run_pipeline(args.dataset_path, args.dataset_type, args.classifier_type)

    print("Evaluation results:")
    print("True positives: " + str(tp))
    print("True negatives: " + str(tn))
    print("False positives: " + str(fp))
    print("False negatives: " + str(fn))
