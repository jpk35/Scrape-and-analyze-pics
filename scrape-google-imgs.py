"""
For a list of google image search terms, save first n images for each term to specified directory
"""
from selenium import webdriver
import time
import requests
import os
from webdriver_manager.chrome import ChromeDriverManager

# if True, prints statements for debugging
debug = True

root = 'directory where you want to save the pictures'  # e.g., 'C:/Users/username/Pictures'
ChromeOptions = webdriver.ChromeOptions()

# these two lines for troubleshooting Chromedriver issues; you may not need them
ChromeOptions.add_argument('--disable-browser-side-navigation')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=ChromeOptions)

# set max page load time (seconds)
driver.set_page_load_timeout(30)


def search_google(search_query):
    """
    :param search_query: Google image search query (string)
    :return: success=1 if able to find and save desired numbers of pics, success=0 if not
    """

    # initialize search url and list for image paths
    browser = driver
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    images_url = []

    # initialize binary "success" variable that function will return
    # this will change to 0 if unable to find and save desired number of pics
    success = 1

    # create folder (folder name is simply set to the search query string here) to store pics for this query
    folder_name = search_query
    path = os.path.join(root, folder_name)
    try:
        os.mkdir(path)
    except OSError as error:
        # ususally this just means directory already exists
        if debug:
            print(error)

    # open browser and begin search
    browser.get(search_url)
    elements = browser.find_elements_by_class_name('rg_i')

    # initiate counts for absolute number of pictures clicked ("count") and number of pics
    # successfully saved ("success_count")
    count = 0
    success_count = 0

    for e in elements:
        # get images source url
        try:
            e.click()
            time.sleep(1)
            element = browser.find_elements_by_class_name('v4dQwb')
            if debug:
                print("clicked pic " + str(count))
        except:
            if debug:
                print("passed pic " + str(count))
            time.sleep(1)

        # Navigate google image search html
        if count == 0:
            big_img = element[0].find_element_by_class_name('n3VNCb')
            if debug:
                print("got element " + str(count))
        else:
            big_img = element[1].find_element_by_class_name('n3VNCb')
            if debug:
                print("got element " + str(count))

        images_url.append(big_img.get_attribute("src"))
        if debug:
            print("added image url " + str(count))

        # write image to file
        try:
            if debug:
                print("in try loop "+ str(count))
            # IMPORTANT: include timeout argument for requests, otherwise code may hang for some queries (with no error)
            response = requests.get(images_url[count], timeout=5)
            if debug:
                print("got image " + str(count))
            if response.status_code == 200:
                # file name set to search query + picture number (absolute) + .jpg (can change file format)
                name = search_query + str(count+1) + ".jpg"
                filename = os.path.join(path, name)
                with open(filename,"wb") as file:
                    file.write(response.content)
                if debug:
                    print("wrote image " + search_query + str(count))
                success_count += 1
            else:
                if debug:
                    print("issue with status code " + search_query + str(count))
                pass
        except:
            if debug:
                print("issue with getting image " + search_query + str(count))
            pass

        count += 1

        # Stop get and save after n (desired number of pictures) successful saves (set to 5 here)
        if success_count == 5:
            break

        # Stop after trying 20 images even if we didn't save n, and set success to 0
        if count == 20:
            success = 0
            break

    return success


if __name__ == "__main__":

    # list of search queries (strings) you want to get and save pictures for
    search_list = ['Annie Edison', 'Dean Pelton']

    # list of queries that program was unable to get and save desired number of pics for
    failures = []

    # scrape pics for each query in search_list, and append list of failures as needed
    # NOTE: Often, queries that fail on the first call of search_google() will succeed if you simply try again in the
    # console
    for query in search_list:
        if search_google(query) == 0:
            failures.append(query)