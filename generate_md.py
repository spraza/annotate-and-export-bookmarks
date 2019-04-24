import json

def populate_rev_index(map, rev_index):
    data = map["data"]
    for rec in data:
        for hashtag in rec["hashtags"]:
            if hashtag not in rev_index:
                rev_index[hashtag] = list()
            rev_index[hashtag].append(rec)

def dump_rec(rev_index, out_file):
    f = open(out_file, 'w')
    for hashtag in rev_index:
        f.write("## " + hashtag)
        f.write('\n')
        for rec in rev_index[hashtag]:
            f.write(rec["title"])
            f.write(" - ")
            f.write("[link](")
            f.write(rec["url"])
            f.write(")")
            f.write('\n\n')
        f.write('\n\n')
    f.close()

def gen_md(map):
    rev_index = dict()
    populate_rev_index(map, rev_index)
    dump_rec(rev_index, "output.md")

# Main
map = json.load(open("annotated-bookmark-candidates.json"))
gen_md(map)