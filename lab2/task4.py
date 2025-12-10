# Напишите программу, которая по информации о том, кто сколько денег потратил,
# определит: кто, кому и сколько денег должен перевести, чтобы расходы всех участников
# похода оказались одинаковыми (с точностью до копейки). Количество переводов при этом
# должно быть как можно меньше.

names = input().split()
n = len(names)

expenses = {name: 0 for name in names}

num_purchases = int(input())

for _ in range(num_purchases):
    data = input().split()
    name = data[0]
    amount = int(data[1])
    expenses[name] += amount

total_expenses = sum(expenses.values())

# средняя сумма
target_per_person = total_expenses / n

# если + баланс, участник переплатил, если - баланс, участник недоплатил
balances = {}
for name in names:
    balance = expenses[name] - target_per_person
    balances[name] = balance

dolshniki = []  # те, кто должен отдать деньги
creditori = []  # те, кто должен получить деньги

for name, balance in balances.items():
    if balance < -0.001:
        dolshniki.append((name, -balance))
    elif balance > 0.001:
        creditori.append((name, balance))

# оба списка сортируются по убыванию суммы
dolshniki.sort(key=lambda x: x[1], reverse=True)
creditori.sort(key=lambda x: x[1], reverse=True)

transfers = []

i = j = 0
while i < len(dolshniki) and j < len(creditori):
    dolshnik, dolshnik_amount = dolshniki[i]
    creditor, credit_amount = creditori[j]

    transfer_amount = min(dolshnik_amount, credit_amount)

    transfers.append((dolshnik, creditor, transfer_amount))

    dolshnik_amount -= transfer_amount
    credit_amount -= transfer_amount

    # проверяем, полностью ли закрыты долг и/или кредит
    if dolshnik_amount < 0.001:
        i += 1
    else:
        dolshniki[i] = (dolshnik, dolshnik_amount)

    if credit_amount < 0.001:
        j += 1
    else:
        creditori[j] = (creditor, credit_amount)

print(len(transfers))
for transfer in transfers:
    dolshnik, creditor, amount = transfer
    print(f"{dolshnik} {creditor} {amount:.2f}")