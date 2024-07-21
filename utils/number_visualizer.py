digits = {
    '0': '0️⃣',
    '1': '1️⃣',
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣',
    '10': '🔟',
}


def view_int(number: [int, str]) -> str:
    if str(number) in digits.keys():
        return digits[str(number)]
    return ''.join([digits[d] for d in str(number)])

