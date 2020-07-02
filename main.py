import pywikibot
from itertools import chain
from pywikibot import pagegenerators
SITE = pywikibot.Site()


def list_maker():
    category1 = pywikibot.Category(SITE,'License review needed')
    gen1 = pagegenerators.CategorizedPageGenerator(category1)
    category2 = pywikibot.Category(SITE,'License review needed (video)')
    gen2 = pagegenerators.CategorizedPageGenerator(category2)
    category3 = pywikibot.Category(SITE,'License review needed (audio)')
    gen3 = pagegenerators.CategorizedPageGenerator(category3)
    gen = chain(gen1, gen2, gen3)
    for page in gen:
        file_name = page.title()
        

def main():
    if not SITE.logged_in():
        SITE.login()

    list_maker()

if __name__ == "__name__":
    try:
        main()
    finally:
        pywikibot.stopme()
