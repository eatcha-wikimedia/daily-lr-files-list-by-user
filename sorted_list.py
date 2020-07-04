import pywikibot
import operator
from pywikibot import pagegenerators

def main(*args):
    global SITE
    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    if not SITE.logged_in():
        SITE.login()
    gen = pagegenerators.CategorizedPageGenerator(pywikibot.Category(SITE,'Files requiring license review sorted by user name'))
    num_name_dict = {}
    for page in gen:
        name = page.title()
        if name.startswith( 'User:EatchaBot/' ):
            print(name)
            file_page = pywikibot.Page(SITE, name)
            content = file_page.get(get_redirect=True, force=True)
            number_of_files = content.count("File:")
            uploader_and_uploads[name] = [number_of_files]

    sorted_num_name_dict = sorted(num_name_dict.items(), key=operator.itemgetter(1))
    for x in sorted_num_name_dict:
        name = x[0]
        count = x[1]
        

    
            

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
