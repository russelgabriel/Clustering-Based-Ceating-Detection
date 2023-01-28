from utility.get_group_freq import get_group_freq

group_freq = get_group_freq()
print("Freq: Total")
for i in range(1,11):
  print("{}: {}".format(i, group_freq[i]["Total"]))