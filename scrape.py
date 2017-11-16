# -*- coding: utf-8 -*-
"""@package scrape
@date Created on nov. 15 09:30 2017
@author samuel_r
"""

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_phrase(jp_words, body):
    jp_phrase = list()
    for word in jp_words:
        type_word = word.get_attribute('data-pos')
        raw_word = word.find_element_by_class_name(
            'japanese_word__text_wrapper')
        hiragana_word = word.find_element_by_class_name(
            'japanese_word__furigana_wrapper')

        link = raw_word.find_element_by_tag_name('a').get_attribute('href')
        new_browser, new_body = load_jisho_page(None, link.split('/')[-1])

        res = get_word(new_body)
        res[1] = hiragana_word.text
        res[2] = type_word
        jp_phrase.append(res)
        new_browser.quit()

    return jp_phrase


def get_word(body):
    w = body.find_element_by_class_name('concept_light-representation')
    raw_word = w.find_element_by_class_name('text').text
    hiragana_word = w.find_element_by_class_name('furigana').text

    translations = body.find_element_by_class_name("meanings-wrapper")
    en_translations = translations.find_elements_by_class_name(
        "meaning-wrapper")
    definitions = list()
    for definition in en_translations:
        definitions.append(definition.text)

    return [raw_word, hiragana_word, None, definitions]


def load_jisho_page(jp_text, link=None):
    browser = webdriver.PhantomJS()
    if jp_text is None:
        browser.get('http://jisho.org/search/' + link)
    else:
        browser.get('https://www.jisho.org')

        input_txt = browser.find_element_by_class_name('text_input')
        input_txt = input_txt.find_element_by_tag_name('input')
        input_txt.send_keys(jp_text)

        browser.find_element_by_id('search_main').find_element_by_tag_name(
            'button').click()

    body = WebDriverWait(browser, 42).until(
        EC.presence_of_element_located((By.ID, "page_container"))
    )
    return browser, body


def get_translation(jp_text):
    browser, body = load_jisho_page(jp_text)

    try:
        jp_words = body.find_element_by_id("zen_bar").find_elements_by_tag_name("li")
    except:
        jp_phrase = [get_word(body)]
    else:
        jp_phrase = get_phrase(jp_words, body)

    browser.quit()
    return jp_phrase
