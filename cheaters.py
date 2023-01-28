from utility.find_cheaters import *

homeworks = ["HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
df = create_df("HW01")
for homework in homeworks:
  df = pd.concat([df, create_df(homework)])

homework_cheaters = find_cheaters_per_hw(df)
all_cheaters = find_all_cheaters(df)
cheater_count = get_cheater_freq(all_cheaters, homework_cheaters)
student_cheat_df = student_cheat_freq(all_cheaters, homework_cheaters)

homeworks = ["HW01", "HW02", "HW03", "HW04", "HW05", "HW06", "HW07", "HW09", "HW10", "HW11"]
hw_cheater_count = []
for homework in homeworks:
  hw_cheater_count.append(len(homework_cheaters[homework]))
hw_cheat_dict = {"Homework": homeworks, "Cheater count": hw_cheater_count}
df = pd.DataFrame(hw_cheat_dict)
print(df.to_string(index=False))

freqs = [x for x in range(1,11)]
cheater_total = []
for freq in freqs:
  cheater_total.append(cheater_count[freq])
cheater_freq_dict = {"Frequency Cheating": freqs, "Cheater Amount": cheater_total}
df = pd.DataFrame(cheater_freq_dict)
print(df.to_string(index=False))

print(student_cheat_df.to_string(index=False))
