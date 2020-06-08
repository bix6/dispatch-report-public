# >>> import csv
# >>> with open('eggs.csv', 'rb') as csvfile:
# ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
# ...     for row in spamreader:
# ...         print ', '.join(row)

import csv
with open('output/2019-01-31_rfv-merged-rgx.csv') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',',quotechar='|')
	text=''
	for row in spamreader:
		# print(row)
		# print(','.join(row))
		# text += ','.join(row)
		# temp = ','.join(row).find(',')
		row = ','.join(row)
		index = row.find(',')
		text += row[index+1:]
		print(row)
	print(text)