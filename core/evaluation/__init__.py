import xlsxwriter


def calculate_metrics(pos_samples, neg_samples, neg_predictions):
    tp = len([x for x in pos_samples if x not in neg_predictions])
    tn = len([x for x in neg_samples if x in neg_predictions])
    fp = len([x for x in neg_samples if x not in neg_predictions])
    fn = len([x for x in pos_samples if x in neg_predictions])
    prec = tp / (tp + fp) if tp + fp != 0 else 0
    rec = tp / (tp + fn) if tp + fn != 0 else 0
    fm = 2 * (prec * rec) / (prec + rec) if prec + rec != 0 else 0
    acc = (tp + tn) / (len(pos_samples) + len(neg_samples))

    return tp, tn, fp, fn, prec, rec, fm, acc


def write_evaluation_results(data):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('evaluation.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    worksheet.write(row, col, 'User')
    worksheet.write(row, col + 1, 'TP')
    worksheet.write(row, col + 2, 'TN')
    worksheet.write(row, col + 3, 'FP')
    worksheet.write(row, col + 4, 'FN')
    worksheet.write(row, col + 5, 'Precision')
    worksheet.write(row, col + 6, 'Recall')
    worksheet.write(row, col + 7, 'F-Measure')
    worksheet.write(row, col + 8, 'Accuracy')
    row += 1

    # Iterate over the data and write it out row by row.
    total_rows = []
    for i in range(len(data)):
        for user, metrics in data[i].items():
            tp, tn, fp, fn, prec, rec, fm, acc = metrics
            worksheet.write(row, col, user)
            worksheet.write(row, col + 1, tp)
            worksheet.write(row, col + 2, tn)
            worksheet.write(row, col + 3, fp)
            worksheet.write(row, col + 4, fn)
            worksheet.write(row, col + 5, prec)
            worksheet.write(row, col + 6, rec)
            worksheet.write(row, col + 7, fm)
            worksheet.write(row, col + 8, acc)
            row += 1

        # Write a total using a formula.
        total_rows.append(row + 1)
        worksheet.write(row, 0, 'Total of round')
        start_row = row - len(data[i]) + 1
        end_row = start_row + len(data[i]) - 1
        worksheet.write(row, 5, '=SUM(F%i:F%i)/%i' % (start_row, end_row, len(data[i])))
        worksheet.write(row, 6, '=SUM(G%i:G%i)/%i' % (start_row, end_row, len(data[i])))
        worksheet.write(row, 7, '=SUM(H%i:H%i)/%i' % (start_row, end_row, len(data[i])))
        worksheet.write(row, 8, '=SUM(I%i:I%i)/%i' % (start_row, end_row, len(data[i])))

        row += 2

    # Sum up results
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 5, '=(%s)/%i' % ('+'.join(['F' + str(r) for r in total_rows]), len(total_rows)))
    worksheet.write(row, 6, '=(%s)/%i' % ('+'.join(['G' + str(r) for r in total_rows]), len(total_rows)))
    worksheet.write(row, 7, '=(%s)/%i' % ('+'.join(['H' + str(r) for r in total_rows]), len(total_rows)))
    worksheet.write(row, 8, '=(%s)/%i' % ('+'.join(['I' + str(r) for r in total_rows]), len(total_rows)))

    workbook.close()
