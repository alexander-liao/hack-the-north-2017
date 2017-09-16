import re
import json

print("Instructions:")
print("When it prompts you for the progression, type the progression as-is")
print("into the prompt. Spaces will all be ignored; for inversions, type all")
print("numbers starting from the top going down. To indicate that the specific")
print("inverse doesn't matter, enter a `?` in place. Separation with dashes is")
print("required. Input the weight manually as an integer. To complete input,")
print("type `end` (case insensitive) into the prompt for the progression, not")
print("the weight.")
print()
print()

data = {
    "progressions": []
}

regex = re.compile(r'([A-Za-z]+)([0-9?]*)')

while True:
    try:
        progression_data_raw = input("Progression >>> ")
        if progression_data_raw.upper() == "END":
            break
        weight = int(input("Weight >>> "))
        progression = {
            "weight": weight,
            "chords": []
        }
        for chord_raw in progression_data_raw.split("-"):
            tp, iv = regex.match(chord_raw).groups()
            if iv in ["?", "", "6", "64"]:
                progression["chords"].append({
                    "type": tp,
                    "inversion": ["?", "", "6", "64"].index(iv) - 1
                })
            elif tp.upper() in ["V", "VII"]:
                if iv in ["7?", "7", "65", "43", "42"]:
                    progression["chords"].append({
                        "type": tp,
                        "inversion": ["7?", "7", "65", "43", "42"].index(iv) - 1
                    })
                else:
                    raise RuntimeError("Must use 7? 7 65 43 42 for seventh chords")
            else:
                raise RuntimeError("Must use ? '' 6 64 for non-V/vii chords")
        data["progressions"].append(progression)
    except Exception as e:
        print(e)
        print("Try again")

print(json.dumps(data, indent = 4))
