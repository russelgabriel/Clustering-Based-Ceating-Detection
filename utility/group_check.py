from utility.get_group_freq import get_group_freq

def group_check():
  group_freq = get_group_freq()
  grouped_students = set()
  for i in range(2,11):
    for allowed in group_freq[i]["Groups"]:
      for person in allowed:
        grouped_students.add(person)
  return grouped_students
          
  