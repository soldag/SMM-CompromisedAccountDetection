import xlsxwriter


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


def writeToXlsx(data, count):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('../evaluation.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    worksheet.write(row, col, 'Durchlauf')
    worksheet.write(row, col + 1, 'TP')
    worksheet.write(row, col + 2, 'TN')
    worksheet.write(row, col + 3, 'FP')
    worksheet.write(row, col + 4, 'FN')
    worksheet.write(row, col + 5, 'Accuracy')
    worksheet.write(row, col + 6, 'Recall')
    worksheet.write(row, col + 7, 'Precision')
    row += 1

    # Iterate over the data and write it out row by row.
    for i, tp, tn, fp, fn, acc, rec, prec in data:
        worksheet.write(row, col, i)
        worksheet.write(row, col + 1, tp)
        worksheet.write(row, col + 2, tn)
        worksheet.write(row, col + 3, fp)
        worksheet.write(row, col + 4, fn)
        worksheet.write(row, col + 5, acc)
        worksheet.write(row, col + 6, rec)
        worksheet.write(row, col + 7, prec)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 5, '=SUM(F2:F' + str(count) + ')/' + str(count-1))
    worksheet.write(row, 6, '=SUM(G2:G' + str(count) + ')/' + str(count-1))
    worksheet.write(row, 7, '=SUM(H2:H' + str(count) + ')/' + str(count-1))

    workbook.close()
