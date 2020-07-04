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
    
    init_text = """{| class="wikitable sortable"\n|-\n
! style="background: #000000; color:   #ffffff ;" | '''Rankings ↕️'''
! style="background: #000000; color:   #ffffff ;" | '''Username ↕️'''
! style="background: #000000; color:   #ffffff ;" | '''Number of files requiring LR ↕️'''
! style="background: #000000; color:   #ffffff ;" | '''Link to gallery of all files requiring LR ↕️ '''
|- style="background:  #ffffff; color:  #000000  ;" """
    
    row_text = ""
    
    serial_no = 0
    for x in sorted_num_name_dict:
        serial_no += 1
        name = x[0]
        count = x[1]
        _row = """\n| %d\n| %s\n| %d\n| link to files\n|- style="background:  #ffffff; color:  #000000  ;" """ % (
            serial_no,
            name,
            
            
            )
        row_text = row_text + 
        


    
            

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
