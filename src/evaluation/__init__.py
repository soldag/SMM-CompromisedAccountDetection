def evaluate(model, samples, labels):
    if len(samples) != len(labels):
        raise ValueError('Number of samples has to equal number of labels!')

    tp = tn = fp = fn = 0
    for i in range(len(samples)):
        label = labels[i]
        prediction = model.predict(samples[i])
        
        if label and prediction:
            tp += 1
        elif not label and not prediction:
            tn += 1
        elif not label and prediction:
            fp += 1
        else:
            fn += 1

    return tp, tn, fp, fn
