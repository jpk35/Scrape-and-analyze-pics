# Scrape-and-analyze-pics
Scrape google image search pictures of people and then analyze them using DeepFace

Use scrape-google-imgs.py to find and save a specified number of images, as found using Google image search, for each person in a list.
These images will be saved in folders labelled with each person's name (as used in Google search).

Use analyze_pic_ethnicity.py to iterate through the saved pictures in each name folder and return ethnicity analysis for each person (from DeepFace).
Analysis will be average over all pictures, and can be easily altered to reflect any of DeepFace's analysis options (e.g., age, expression).
