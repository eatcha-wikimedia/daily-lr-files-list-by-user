# -*- coding: utf-8 -*-
import multiprocessing
import time
import pywikibot
import re
from datetime import datetime
from pywikibot import pagegenerators
import concurrent.futures
import mwclient
site = mwclient.Site(('https', 'commons.wikimedia.org'))
site.login('EatchaBot', 'hadikjhadlkjdlkashfdsjgahufisdj')

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
def example_func(page):
    global __count
    __count += 1
    file_name = page.name
    print("%d - %s" % (__count,file_name))
    # if file_name.startswith("File:"):
    #     __count += 1
    #     print("%d - %s" % (__count, file_name))
    #     Uploader = uploader(file_name, link=False)
    #     user_review_subpage_name = "User:EatchaBot/Files-requiring-license-review-gallery-uploaded-by/%s" % Uploader
    #     user_review_subpage = pywikibot.Page(SITE, user_review_subpage_name)
    #     try:
    #         user_review_subpage_old_text = user_review_subpage.get(get_redirect=True, force=True)
    #     except pywikibot.NoPage:
    #         user_review_subpage_old_text = """<p style="border-top: 2px solid #000;border-bottom: 2px solid #000;background-color: #6f6e6d ;color:#ffffff" align="center">&#8594; Sorted list available at [[User:EatchaBot/Files-requiring-license-review-sorted-list|<span style="color:#ffffff">'''User:EatchaBot/Files-requiring-license-review-sorted-list'''</span>]].</p>\n<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"""
        
    #     if file_name in user_review_subpage_old_text:
    #         return
        
    #     if (user_review_subpage_old_text.find('<gallery showfilename=yes>') != -1):
    #         pass
    #     else:
    #         user_review_subpage_old_text = """<p style="border-top: 2px solid #000;border-bottom: 2px solid #000;background-color: #6f6e6d ;color:#ffffff" align="center">&#8594; Sorted list available at [[User:EatchaBot/Files-requiring-license-review-sorted-list|<span style="color:#ffffff">'''User:EatchaBot/Files-requiring-license-review-sorted-list'''</span>]].</p>\n<gallery showfilename=yes>\n</gallery>\n[[Category:Files requiring license review sorted by user name]]"""

    #     _count = user_review_subpage_old_text.count("File:") + 1
        
    #     user_review_subpage_new_text = re.sub("</gallery>", "%s|%s\n</gallery>" % (file_name, _count,) , user_review_subpage_old_text)
    #     user_review_subpage_EditSummary = "Adding [[%s]]" % (file_name)
    #     if user_review_subpage_old_text == user_review_subpage_new_text:
    #         return
    #     try:
    #         commit(user_review_subpage_old_text, user_review_subpage_new_text, user_review_subpage, "{0}".format(user_review_subpage_EditSummary))
    #     except pywikibot.LockedPage as error:
    #         return


def list_maker():
    gen1 = site.Categories['License review needed']

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            executor.map(example_func, gen1)

def main(*args):
    global SITE
    args = pywikibot.handle_args(*args)
    SITE = pywikibot.Site()
    if not SITE.logged_in():
        SITE.login()

    proc = multiprocessing.Process(target=list_maker, name="ListMaker")
    proc.start()
    time_to_wait = 2 #In hours
    proc.join(time_to_wait*3600)
    if proc.is_alive():
        print ("list_maker is takin too mcuh time, force killing it.")
        proc.terminate()
        proc.join()


if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
