"""
Given folder of images of people, returns dataframe with average ethnicity predictions (from DeepFace) for each
person
"""
from deepface import DeepFace
import os
import pandas as pd
import unicodedata2 as unicodedata

# pics = 'directory where pictures to analyze are located'  # e.g., 'C:/Users/username/Pictures'
pics = 'C:/Users/jpkad/Pictures'

# if True, prints statements for debugging
debug = True


def predict_ethn(img_path):
    """
    :param img_path: location of image to be analyzed
    :return: dict with percent "likelihood" of each ethnicity (asian, indian, black, white, middle_eastern,
    latino_hispanic) for the face identified in the photo
    """
    ethn_predictions = []
    try:
        img = DeepFace.analyze(img_path=img_path, actions=['race'])
        ethn_predictions = img['race']
    except:
        if debug:
            print('problem with DeepFace for ' + img_path)
    return ethn_predictions


# create dataframe to hold average predicted ethnicity data for each person
columns_list = ['Name', 'avg prediction asian', 'avg prediction indian', 'avg prediction black',
                'avg prediction white', 'avg prediction middle eastern', 'avg prediction latino hispanic',
                'missing pics']
df = pd.DataFrame(columns=columns_list)


def analyze_pics(name):
    """
    :param name: person's name (must match name of folder containing their pictures)
    :return: dataframe with columns as in df and one row with average predicted % for each race, to be appended to df
    """

    # location of folder with pictures of person to be analyzed
    loc = os.path.join(pics, name)

    # to track instances where DeepFace cannot analyze all pics for the given person (will be equal to number of
    # pictures not able to be analyzed in the given folder)
    missing_pics = 0

    # initialize df row (first column is person's name)
    row = [name]

    # initialize list of % predictions for each ethnicity that DeepFace assesses
    asian = []
    indian = []
    black = []
    white = []
    middle_eastern = []
    latino_hispanic = []
    ethnicities = ['asian', 'indian', 'black', 'white', 'middle_eastern', 'latino_hispanic']
    ethnicities_lists = [asian, indian, black, white, middle_eastern, latino_hispanic]

    # iterate through all pics of the person and create list with predicted %s for each ethnicity for each picture
    # (one list per ethnicity)
    for file in os.listdir(loc):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            img_path = os.path.join(loc, filename)
            # analyzed will have dict with predicted % for each ethnicity
            analyzed = predict_ethn(img_path)
            if analyzed != []:
                # iterate through ethnicities as strings
                for ethn in ethnicities:
                    key = ethn.replace('_', ' ')
                    # locals()[race] calls current string (e.g., 'asian') as a variable
                    locals()[ethn] += [analyzed[key]]
                    if debug:
                        print(locals()[ethn])
            else:
                missing_pics += 1
        else:
            pass

    # average % predictions for each race over the 5 pics (or however many were able to be collected) and
    # put them into a row to populate the dataframe columns for this player
    for lst in ethnicities_lists:
        if len(lst) > 0:
            lst = sum(lst) / len(lst)
            row += [lst]
        else:
            row += ['na']
        if debug:
            print(lst)

    if debug:
        print(row)

    # last column of dataframe reports how many pics were not able to be analyzed
    row += [missing_pics]

    df2 = pd.DataFrame([row], columns=columns_list)
    if debug:
        print(df2)

    return df2


if __name__ == "__main__":

    # list of people's names with pictures to analyze
    to_analyze = ['Annie Edison', 'Dean Pelton']

    for name in to_analyze:
        df = df.append(analyze_pics(name))