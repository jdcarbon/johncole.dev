"""Starting point: a working but monolithic study-time tracker."""

study_minutes = [45, 30, 60, 0, 25, 50, 40]
goal = 45

total = 0
for value in study_minutes:
    total = total + value

average = total / len(study_minutes)

days_met = 0
for value in study_minutes:
    if value >= goal:
        days_met = days_met + 1

print("Total:", total, "minutes")
print("Daily average:", average, "minutes")
print("Days meeting goal (", goal, "):", days_met)
