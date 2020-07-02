import pywikibot
from itertools import chain
from pywikibot import pagegenerators
SITE = pywikibot.Site()

def uploader(filename, link=True):
    """User that uploaded the file."""
    history = (pywikibot.Page(SITE, filename)).revisions(reverse=True, total=1)
    for info in history:
        username = (info.user)
    if not history:
        return "Unknown"
    if link:
        return "[[User:%s|%s]]" % (username, username)
    return username

def list_maker():

    category1 = pywikibot.Category(SITE,'License review needed')
    gen1 = pagegenerators.CategorizedPageGenerator(category1)
    category2 = pywikibot.Category(SITE,'License review needed (video)')
    gen2 = pagegenerators.CategorizedPageGenerator(category2)
    category3 = pywikibot.Category(SITE,'License review needed (audio)')
    gen3 = pagegenerators.CategorizedPageGenerator(category3)
    gen = chain(gen1, gen2, gen3)

    uploader_and_uploads = {}

    for page in gen:

        file_name = page.title()
        if file_name.startswith("File:"):

            Uploader = uploader(file_name, link=False)
            
            if uploader_and_uploads.get(Uploader):
                files_list = uploader_and_uploads.get(Uploader)
                files_list.append(file_name)
                uploader_and_uploads[Uploader] = files_list
            else:
                uploader_and_uploads[Uploader] = [file_name]
            
        

def main():
    if not SITE.logged_in():
        SITE.login()

    list_maker()

if __name__ == "__name__":
    try:
        main()
    finally:
        pywikibot.stopme()
