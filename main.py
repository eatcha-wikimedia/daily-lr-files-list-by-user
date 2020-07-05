# -*- coding: utf-8 -*-
import pywikibot
import re
from itertools import chain
from datetime import datetime
from pywikibot import pagegenerators

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

def list_maker():
    
    category1 = pywikibot.Category(SITE,'License review needed')
    gen1 = pagegenerators.CategorizedPageGenerator(category1)
    category2 = pywikibot.Category(SITE,'License review needed (video)')
    gen2 = pagegenerators.CategorizedPageGenerator(category2)
    category3 = pywikibot.Category(SITE,'License review needed (audio)')
    gen3 = pagegenerators.CategorizedPageGenerator(category3)
    gen = chain(gen1, gen2, gen3)

    uploader_and_uploads = {}
    __count = 0
    for page in gen:
        file_name = page.title()
        if file_name.startswith("File:"):
            __count += 1 
            print("%d - %s" % (__count, file_name))
            Uploader = uploader(file_name, link=False)
            user_review_subpage_name = "User:EatchaBot/Files-requiring-license-review-gallery-uploaded-by/%s" % Uploader
            user_review_subpage = pywikibot.Page(SITE, user_review_subpage_name)
            try:
                user_review_subpage_old_text = user_review_subpage.get(get_redirect=True, force=True)
            except pywikibot.NoPage:
                user_review_subpage_old_text = """<p style="border-top: 2px solid #000;border-bottom: 2px solid #000;background-color: #6f6e6d ;color:#ffffff" align="center">&#8594; Sorted list available at [[User:EatchaBot/Files-requiring-license-review-sorted-list|<span style="color:#ffffff">'''User:EatchaBot/Files-requiring-license-review-sorted-list'''</span>]].</p>\n<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"""
            
            if file_name in user_review_subpage_old_text:
                continue
            
            if (user_review_subpage_old_text.find('<gallery showfilename=yes>') != -1):
                pass
            else:
                user_review_subpage_old_text = "<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"
            
            m = re.search(r"(?ms)<gallery showfilename=yes>(.*)</gallery>", user_review_subpage_old_text)
            try:
                _count = m.group(0).count("\n")
            except:
                _count = 1
            
            user_review_subpage_new_text = re.sub("</gallery>", "%s|%s\n</gallery>" % (file_name, _count,) , user_review_subpage_old_text)
            user_review_subpage_EditSummary = "Adding [[%s]]" % (file_name)
            try:
                commit(user_review_subpage_old_text, user_review_subpage_new_text, user_review_subpage, "{0}".format(user_review_subpage_EditSummary))
            except pywikibot.LockedPage as error:
                pass

def main(*args):
    global SITE
    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    if not SITE.logged_in():
        SITE.login()

    list_maker()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
