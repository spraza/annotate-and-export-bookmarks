import json
import webbrowser
import datetime
from pathlib import Path

def populate_safari(map, results):
    # Populate map with required fields
    if "all_hashtags" not in results:
        results["all_hashtags"] = list()
    if "data" not in results:
        results["data"] = list()    
    url_field = "URLString"
    if url_field in map:
        temp_map = dict()
        temp_map["title"] = map["URIDictionary"]["title"].encode("ascii", "ignore").decode()
        temp_map["url"] = map[url_field]
        temp_map["hashtags"] = list()
        temp_map["browser"] = "safari"
        temp_map["ignore"] = False
        results["data"].append(temp_map)
    for key in map.keys():
        val = map[key]
        if type(val) is dict:
            populate_safari(val, results)
        elif type(val) is list:
            for el in val:
                if type(el) is dict:
                    populate_safari(el, results)

def populate_firefox(map, results):
    # Populate map with required fields
    if "all_hashtags" not in results:
        results["all_hashtags"] = list()
    if "data" not in results:
        results["data"] = list()    
    url_field = "uri"
    if url_field in map:
        temp_map = dict()
        temp_map["title"] = map["title"].encode("ascii", "ignore").decode()
        temp_map["url"] = map[url_field]
        temp_map["hashtags"] = list()
        temp_map["browser"] = "firefox"
        temp_map["ignore"] = False
        results["data"].append(temp_map)
    for key in map.keys():
        val = map[key]
        if type(val) is dict:
            populate_firefox(val, results)
        elif type(val) is list:
            for el in val:
                if type(el) is dict:
                    populate_firefox(el, results)

# bookmark_file_name is the input file
# candidate_file_name is the output file
def write_candidates(safari_bookmark_file_name, firefox_bookmark_file_name, candidate_file_name):
    # Read bookmarks file given to us and setup results output    
    results = dict()

    # Add datetime to results before serializing
    results["datetime"] = datetime.datetime.now().strftime("%I:%M %p on %B %d, %Y")

    # Populate candidates in memory
    safari_bookmarks_map = json.load(open(safari_bookmark_file_name))
    firefox_bookmarks_map = json.load(open(firefox_bookmark_file_name))
    populate_safari(safari_bookmarks_map, results)
    populate_firefox(firefox_bookmarks_map, results)

    # Serialize or write candidates to disk in json format
    json.dump(results, open(candidate_file_name, 'w'), indent=True)

def fill_hashtags(candidate_file_name, browser):
    browser = webbrowser.get("firefox")
    candidates = json.load(open(candidate_file_name))
    all_hashtags = candidates["all_hashtags"]
    for rec in candidates["data"]:
        if not rec["hashtags"] and not rec["ignore"]:
            browser.open_new_tab(rec["url"])
            for i in range(len(all_hashtags)):
                print(str(i) + ": " + all_hashtags[i])
            hashtags = input("hashtags: ")
            if hashtags:
                hashtags = [hashtag.strip() for hashtag in hashtags.split(',')]
                hashtags = [hashtag.encode("ascii", "ignore").decode() for hashtag in hashtags]
                for i in range(len(hashtags)):
                    if hashtags[i].isdigit():
                        hashtags[i] = all_hashtags[int(hashtags[i])]
                    else:
                        all_hashtags.append(hashtags[i])            
                rec["hashtags"] = hashtags
            else:
                rec["ignore"] = True
            json.dump(candidates, open(candidate_file_name, 'w'), indent=True)

# Main
candidate_file_name = "annotated-bookmark-candidates.json"
safari_bookmark_file_name = "safari-bookmarks.json"
firefox_bookmark_file_name = "firefox-bookmarks.json"
if not Path(candidate_file_name).is_file():
    write_candidates(safari_bookmark_file_name, firefox_bookmark_file_name, candidate_file_name)
    print("Wrote candidates to: " + candidate_file_name)
fill_hashtags(candidate_file_name, "firefox")

