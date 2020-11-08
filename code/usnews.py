import csv
f = open("usnews", "r")
lines = [x.strip() for x in f]
lines1 = [line for line in lines if len(line)>0][1:]
records = [lines1[i:i+3] for i in range(0,len(lines1)-2,3)]
csv_records = [','.join(item) for item in records]
csv_records_final = [item.split(',') for item in csv_records]
f.close() 

'''writer=csv.writer(open('us_news_rankings.csv','w'))
for record in csv_records:
    writer.writerow([record])'''
    
with open('us_news_rankings.csv','w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for record in csv_records_final:
        writer.writerow(record)