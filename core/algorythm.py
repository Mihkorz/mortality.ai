import os
import csv

BASE = os.path.dirname(os.path.abspath(__file__))

kwargs = {"gender":1,               #0 = female, 1 = male 
          "country":"Germany",      #country names as in 2 column of cntr.txt. For example France, Nigeria (case not sensitive)
          "age":23,                 #integer or float 0 - 999
          "height":1.65,            #float height in meters
          "weight":65,              #float weight in kilograms
          "alcohol":1,              #integer. Different meaning of value for men and women: 
                                    #For men  0 = non-drinker, 1 = < 1 drink/month, 2 = 0-4/week, 3 = 5-9/week, 4 = 10-24/week, 5 = binger 
                                    #For women  0 = non-drinker, 1 = < 1 drink/month, 2 = 0-2/week, 3 = 3-5/week, 4 = 6-17/week, 5 = binger
          "smoking":1,              #integer 0 = never smoked, 1 = formaer smoker, 2 = current light smoker, 3 = current heavy smoker
          "activity":1,             #integer 0 = low activity, 1 = moderate, 2 = high
          "social_status":True,     #boolean. True = good social life, False = poor social life
          "mental":False}           #boolean. True = active mental illnes, False = no active mental illness

def ages_left(**kwargs):
    expected_longevity = country_data(kwargs["country"], kwargs["age"], kwargs["gender"])
    expected_longevity += bmi_effect(kwargs["height"], kwargs["weight"], kwargs["gender"])
    expected_longevity += alcohol_effect(kwargs["alcohol"], kwargs["gender"])
    expected_longevity += smoking_effect(kwargs["smoking"], kwargs["gender"])
    expected_longevity += activity_effect(kwargs["activity"], kwargs["gender"])
    if not kwargs["social_status"]:
        expected_longevity -= 1.3
    if kwargs["mental"]:
        expected_longevity += [-15.9, -12.0]["gender"]
    
    return expected_longevity



def activity_effect(activity, gender):
    activity_dict = {2: [3.3, 2.9], 1: [2.7, 1.8], 0: [-1.4, -1.5]}
    return activity_dict[activity][gender]


def smoking_effect(smoking, gender):
    smoking_dict = {0: [2.2, 3.2], 1: [-1.9, -0.1], 2: [-4.1, -4.5], 3: [-9.0, -8.6]}
    return smoking_dict[smoking][gender]


def alcohol_effect(alcohol, gender):
    alcohol_dict = {0: [-1.7, -1.5], 1: [-0.1, -0.8], 2: [1.8, 1.0], 3: [3.5, 2.6], 4: [1.5, 0.5], 5: [-1.7, -1.7]}
    return alcohol_dict[alcohol][gender]


def country_data(person_country, age, gender):
    with open(os.path.join(BASE, "cntr.txt")) as countries_file:
        for country in countries_file:
            country_entry = country.split("\t")
            if country_entry[0].lower() == person_country.lower():
                country_name = "cleaned_data/{}.txt".format(country_entry[0])
                break

    with open(os.path.join(BASE,country_name)) as person_country_file:
        for line in person_country_file:
            splitted_line = [float(x) for x in line[:-1].split("\t")]
            line_dict = dict(zip(["min", "max", 0, 1], splitted_line))
            if line_dict["min"] <= age <= line_dict["max"]:
                return line_dict[gender]
    


def bmi_effect(height, weight, gender):
    bmi = weight/(height**2)
    bmi_effects = {(0, 18.5): (-2.7, -5.9), (18.5, 25): (0, 0), (25, 30): (-1, 0), (30, 35): (-3.8, -1), (35, 250): (-7.8, -3.5)}
    for effect in bmi_effects:
        if effect[0] < bmi < effect[1]:
                return bmi_effects[effect][gender]
            

def crop_countries():
    for country_filename in os.listdir("data"):
        out_file = open("cleaned_data/" + country_filename, "w")
        header = True
        with open("data/" + country_filename) as country_csv:
            country_reader = csv.reader(country_csv, delimiter=',', quotechar='"')
            for line in country_reader:
                if header:
                    header = False
                if line[0][:2] == "ex":
                    out_listed_line = get_age(line[1]) + line[2:4]
                    out_line = "\t".join(out_listed_line) + "\n"
                    out_file.write(out_line)
        out_file.close()


def get_age(age_field):
    if "&lt;" in age_field:
        return["0", "1"]
    elif "100+" in age_field:
        return ["100", "999"]
    age_field = age_field.replace(" years", "").strip()
    ages = age_field.split("-")
    return ages


