import csv

datasets = ["Deaths", "Confirmed", "Recovered"]

for dataset in datasets:
    with open(f'time_series_19-covid-{dataset}.csv') as csv_file:
        with open(f'time_series_19-covid-{dataset}-Processes.csv', 'w') as csv_file_out:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            dates = None
            for row in csv_reader:
                if line_count == 0:
                    dates = row
                    csv_file_out.write(';'.join(["Provice", "Country", "Lat", "Long", "Date", dataset]) + "\n")
                    line_count += 1
                    continue
                for i in range(4, 53):
                    csv_file_out.write(';'.join([row[0], row[1], row[2], row[3], dates[i], row[i]]) + "\n")
                line_count += 1
