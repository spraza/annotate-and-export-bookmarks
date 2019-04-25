An automated annotated tool I made for myself to annotate hundreds of bookmarks I've across different browsers e.g. Firefox and Safari.

After annotation, I wrote a script to output a markdown file, which I'll use on my website [here](http://spraza.com/knowledge/).

Here's how I did it:

First step was to **get bookmarks in *some* format**. Different browsers have different data formats when it comes to memory object serialization to disk. For Safari, this is a [plist](https://en.wikipedia.org/wiki/Property_list) file, and for Firefox, this is a json file. 

For safari, I read [this](http://amitp.blogspot.com/2014/05/extracting-safaris-reading-list.html) link to get the `plist` file. For firefox, exporting json data is [simple](https://support.mozilla.org/en-US/kb/restore-bookmarks-from-backup-or-move-them).

Second step was to **blend or combine all browser bookmarks** into a single json file. 

Once that's done, the third step is that I **annotate that bookmarks file automatically** by adding hashtags for each bookmark. The way it works is that the python program automatically opens every bookmark, and then asks for hashtags, which I can enter. The program then updates the file, and does the same for the rest of the bookmarks. There are certain features here and there e.g. everytime you enter hashtags, you can see previous hashtags, so you can reuse them (by their indexed number that's also displayed). You can also leave the bookmarks as blank. 

The second and third step are done by `tag_bookmarks.py`.

Finally, the fourth step is to **generate the output markdown file** from the annotated bookmarks file, which is what `generate_md.py` does.










