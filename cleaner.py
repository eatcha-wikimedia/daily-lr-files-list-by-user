import pywikibot
from pywikibot import pagegenerators
import concurrent.futures

def worker(page):
    name = page.title()
    if name.startswith( 'User:EatchaBot/' ):
        print(name)
        file_page = pywikibot.Page(SITE, name)
        old_text = file_page.get(get_redirect=True, force=True)
        new_text = ""
        EditSummary = "flushed old list, will generate new list every week."
        if new_text == old_text:
            pass
        try:
            page.put(new_text, summary=EditSummary, watch=True, minor=False)
        except:
            pass


def main(*args):
    global SITE
    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    if not SITE.logged_in():
        SITE.login()
    gen = pagegenerators.CategorizedPageGenerator(pywikibot.Category(SITE,'Files requiring license review sorted by user name'))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(worker, gen)

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
