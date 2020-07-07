# -*- coding: utf-8 -*-
import pywikibot
import re
from datetime import datetime
from pywikibot import pagegenerators
import concurrent.futures

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
    """output some text to the consoloe / log."""
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

def dict_maker(page):
    file_name = page.title()
    if file_name.startswith("File:"):
        global __count
        __count += 1 
        print("%d - %s" % (__count, file_name))

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

def operator(param):
    Uploader = param[0]
    file_list = param[1]
    print(Uploader)

    user_review_subpage_name = "User:EatchaBot/Files-requiring-license-review-gallery-uploaded-by/%s" % Uploader
    user_review_subpage = pywikibot.Page(SITE, user_review_subpage_name)
    try:
        user_review_subpage_old_text = user_review_subpage.get(get_redirect=True, force=True)
    except pywikibot.NoPage:
        user_review_subpage_old_text = """<p style="border-top: 2px solid #000;border-bottom: 2px solid #000;background-color: #6f6e6d ;color:#ffffff" align="center">&#8594; Sorted list available at [[User:EatchaBot/Files-requiring-license-review-sorted-list|<span style="color:#ffffff">'''User:EatchaBot/Files-requiring-license-review-sorted-list'''</span>]].</p>\n<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"""
    
    if (user_review_subpage_old_text.find('<gallery showfilename=yes>') != -1):
        pass
    else:
        user_review_subpage_old_text = """<p style="border-top: 2px solid #000;border-bottom: 2px solid #000;background-color: #6f6e6d ;color:#ffffff" align="center">&#8594; Sorted list available at [[User:EatchaBot/Files-requiring-license-review-sorted-list|<span style="color:#ffffff">'''User:EatchaBot/Files-requiring-license-review-sorted-list'''</span>]].</p>\n<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"""
    
    _count = user_review_subpage_old_text.count("File:")
    _text = ""

    for file_name in file_list:

        if file_name in user_review_subpage_old_text:
            continue

        _count += 1
        row =  "%s|%s\n" % (file_name, _count)
        _text = _text + row
    
    _text = _text + "</gallery>"

    new_text = user_review_subpage_old_text.replace("</gallery>", _text)
    user_review_subpage_EditSummary = "Adding %d files" % (len(file_list))

    try:
        commit(user_review_subpage_old_text, new_text, user_review_subpage, "{0}".format(user_review_subpage_EditSummary))
    except Exception as e:
        print(e)
        continue

def gallery_maker():

    category1 = pywikibot.Category(SITE,'License review needed (video)')
    gen1 = pagegenerators.CategorizedPageGenerator(category1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            executor.map(dict_maker, gen1)

    category2 = pywikibot.Category(SITE,'License review needed (audio)')
    gen3 = pagegenerators.CategorizedPageGenerator(category2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            executor.map(dict_maker, gen3)

    global uploader_files_list_dict
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        executor.map(operator, uploader_files_list_dict.items())


    
def main(*args):
    global SITE
    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    if not SITE.logged_in():
        SITE.login()

    gallery_maker()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
