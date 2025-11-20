CURRENT_YEAR = 2025 #constants
MAX_HUMAN_AGE = 150 # let's assume the theoretical limit of the human lifespan is 150 years

def name_input():
    """Get validated username (non-empty)"""
    while True:
        us_name = input("Please enter your full name: ").strip()
        if not us_name:
            continue
        return us_name

def age_input():
    """Get validated birth year and return current age"""
    while True:
        birth_year_str = input("Please enter your birth year: ").strip()
        try:
            birth_year = int(birth_year_str)
        except ValueError:
            print("Enter a valid (numeric) year")
            continue
        if birth_year > CURRENT_YEAR:
            print("Enter a valid year (not in future)")
            continue
        elif birth_year < 0:
            print("Enter a valid year (not a negative one)")
            continue
        elif CURRENT_YEAR - birth_year > MAX_HUMAN_AGE:
            print("Enter a valid year (humans can't live for so long)")
            continue
        cur_age = CURRENT_YEAR - birth_year
        return cur_age

def generate_profile(a):
    """Return life stage based on age"""
    if 0 <= a <= 12:
        return "Child"
    elif 13 <= a <= 19:
        return "Teenager"
    elif a >= 20:
        return "Adult"

def add_hobbies(hobbie_s):
    """Collect hobbies until user types 'stop'"""
    while True:
        hobby = input("Enter a favorite hobby or  type 'stop' to finish: ").strip()
        if not hobby:
            print("Enter any hobby")
            continue
        elif hobby.lower() == "stop":
            break
        hobbie_s.append(hobby)

def generate_message(use_profile):
    """Create formatted profile summary"""
    required_keys = ['name', 'age', 'stage', 'hobbies']
    for x in required_keys:
        if x not in use_profile:
            return f"Error: {x} missing"
    mes =  ("Profile Summary: \n"
           f"Name: {use_profile['name']}\n"
           f"Age: {use_profile['age']}\n"
           f"Stage: {use_profile['stage']}\n")
    if not use_profile['hobbies']:
        mes += "You didn't mention any hobbies."
    else:
        mes += f"Favorite hobbies ({len(use_profile['hobbies'])}):\n"
        for x in use_profile['hobbies']:
            mes += f"- {x}\n"
    return mes

user_name = name_input()
current_age = age_input()
life_stage = generate_profile(current_age)
hobbies = []
add_hobbies(hobbies)
user_profile = {'name': user_name, 'age': current_age, 'stage': life_stage, 'hobbies': hobbies}
print(generate_message(user_profile))
