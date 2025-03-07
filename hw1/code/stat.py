from collections import Counter

print("--- c=0.1 ----")
with open('UCTout_c=0.1.txt', 'r') as file:
    numbers_1 = [int(line.strip()) for line in file if line.strip().isdigit()]
freq_1 = Counter(numbers_1)
for num, count in sorted(freq_1.items()):
    print(f"数字 {num} 出现了 {count} 次")

print("--- c=5.0 ----")
with open('UCTout_c=5.0.txt', 'r') as file:
    numbers_2 = [int(line.strip()) for line in file if line.strip().isdigit()]
freq_2 = Counter(numbers_2)
for num, count in sorted(freq_2.items()):
    print(f"数字 {num} 出现了 {count} 次")