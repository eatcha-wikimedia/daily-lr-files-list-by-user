# -*- coding: utf-8 -*-
import re
import pywikibot
import operator
from pywikibot import pagegenerators
from datetime import datetime


# For chaining the files in images,video and audio lr Categories.
from itertools import chain

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

def out(text, newline=True, date=False, color=None):
    """output some text to the console."""
    if color:
        text = "\03{%s}%s\03{default}" % (color, text)
    dstr = (
        "%s: " % datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if date
        else ""
    )
    pywikibot.stdout("%s%s" % (dstr, text), newline=newline)

def commit(old_text, new_text, page, summary):
    """Show diff and submit text to page."""
    out("\nAbout to make changes at : '%s'" % page.title())
    pywikibot.showDiff(old_text, new_text)
    page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)


__count = 0
uploader_files_list_dict = {}

def dict_maker_pywikibot(page):
    file_name = page.title()
    if file_name.startswith("File:"):
        global __count
        __count += 1 
        out("%d - %s" % (__count, file_name))

        Uploader = uploader(file_name, link=False)
        global uploader_files_list_dict
        if uploader_files_list_dict.get(Uploader):
            list_ = uploader_files_list_dict.get(Uploader)
            list_.append(file_name)
            uploader_files_list_dict[Uploader] = list_
        else:
            _list = []
            _list.append(file_name)
            uploader_files_list_dict[Uploader] = _list

num_name_dict = {}
def gallery_operator(param):
    Uploader = param[0]
    file_list = param[1]
    number_of_files = len(file_list)
    out(Uploader)
    global num_name_dict
    num_name_dict[Uploader] = [number_of_files]

    user_review_subpage_name = "User:EatchaBot/Files-requiring-license-review-gallery-uploaded-by/%s" % Uploader
    user_review_subpage = pywikibot.Page(SITE, user_review_subpage_name)
    template = """<p style="border-top: 2px solid #000;border-bottom: 2px solid #000;background-color: #6f6e6d ;color:#ffffff" align="center">&#8594; Sorted list available at [[User:EatchaBot/Files-requiring-license-review-sorted-list|<span style="color:#ffffff">'''User:EatchaBot/Files-requiring-license-review-sorted-list'''</span>]].</p>\n<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"""
    
    _count = 0
    _text = ""
    for file_name in file_list:
        _count += 1
        row =  "%s|%s\n" % (file_name, _count)
        _text = _text + row
    _text = _text + "</gallery>"

    new_text = template.replace("</gallery>", _text)
    EditSummary = "Adding %d files" % (number_of_files)

    if template == new_text:
        return

    try:
        commit("", new_text, user_review_subpage, "{0}".format(EditSummary))
    except Exception as e:
        out(e)
        return

def gallery_maker():

    category_video = pywikibot.Category(SITE,'License review needed (video)')
    gen_video = pagegenerators.CategorizedPageGenerator(category_video)
    for page in gen_video:
        dict_maker_pywikibot(page)

    category_audio = pywikibot.Category(SITE,'License review needed (audio)')
    gen_audio = pagegenerators.CategorizedPageGenerator(category_audio)
    for page in gen_audio:
        dict_maker_pywikibot(page)

    category_image = pywikibot.Category(SITE, 'License review needed')
    gen_image = pagegenerators.CategorizedPageGenerator(category_image)
    try:
        for page in gen_image:
            dict_maker_pywikibot(page)
    except Exception as e:
        out(e, color="red")
    

    global uploader_files_list_dict
    for param in uploader_files_list_dict.items():
        gallery_operator(param)

def list_maker():
    print("sorting")
    global num_name_dict
    sorted_num_name_dict = sorted(num_name_dict.items(), key=operator.itemgetter(1))
    
    init_text = """{| class="wikitable sortable"\n|-\n
! style="background: #000000; color:   #ffffff ;" | '''Rankings ↕️'''
! style="background: #000000; color:   #ffffff ;" | '''Username ↕️'''
! style="background: #000000; color:   #ffffff ;" | '''Number of files requiring LR ↕️'''
! style="background: #000000; color:   #ffffff ;" | '''Link to gallery of all files requiring LR ↕️ '''
|- style="background:  #ffffff; color:  #000000  ;" """
    
    row_text = ""
    serial_no = len(sorted_num_name_dict)
    print ("creating rows")
    for x in sorted_num_name_dict:
        gallery_page = x[0]
        name = gallery_page.replace("User:EatchaBot/Files-requiring-license-review-gallery-uploaded-by/","")
        count = x[1][0]
        print (count)
        _row = """\n| %d\n| {{noping|%s}}\n| %d\n| [[User:EatchaBot/Files-requiring-license-review-gallery-uploaded-by/%s|Gallery for %s's files]]\n|- style="background:  #ffffff; color:  #000000  ;" """ % (
            serial_no,
            name,
            count,
            name,
            name
            )
        serial_no -= 1
        row_text =  _row + row_text
    new_text = init_text + row_text + "\n|}"
    list_page_name = "User:EatchaBot/Files-requiring-license-review-sorted-list"
    list_page = pywikibot.Page(SITE, list_page_name)
    summary = "list of files"
    print ("saving list")
    list_page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)
    print ("OK")


def main(*args):
    global SITE
    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    if not SITE.logged_in():
        SITE.login()

    # Fills the galleries with current files

    gallery_maker()



    # Updates the list by username
    list_maker()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
