import sys
import csv

with open(sys.argv[2], "w") as writer:
    with open(sys.argv[1], "rb") as f:
        r = csv.reader(f)
        for row in r:
            for col in row:
                if col:
                    writer.write(col + '\n')
                break
