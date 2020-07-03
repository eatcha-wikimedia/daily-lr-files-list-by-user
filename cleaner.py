import pywikibot
from pywikibot import pagegenerators

SITE = pywikibot.Site()

if not SITE.logged_in():
  SITE.login()


category1 = pywikibot.Category(SITE,'Files requiring license review sorted by user name')
gen1 = pagegenerators.CategorizedPageGenerator(category1)

def commit(old_text, new_text, page, comment):
  if new_text == old_text:return
  page.put(new_text, summary=comment, watch=False, minor=False)

def main():
  for page in gen1:
    namefile = page.title()
    if namefile.startswith( 'User:EatchaBot/' ):
      print(namefile)
      file_page = pywikibot.Page(SITE, namefile)
      old_text = file_page.get(get_redirect=True, force=True)
      new_text = ""
      EditSummary = "flushed old list, will generate new list every week."
      commit(old_text, new_text, file_page, "{0}".format(EditSummary))

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
