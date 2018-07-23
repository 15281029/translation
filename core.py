# -*- coding: utf-8 -*-

import json
from collections import namedtuple

import requests

PBMT = {
    "Afrikaans (南非荷兰语)": "af",
    "Albanian (阿尔巴尼亚语)": "sq",
    "Amharic (阿姆哈拉语)": "am",
    "Arabic (阿拉伯语)": "ar",
    "Armenian (亚美尼亚语)": "hy",
    "Azeerbaijani (南非语)": "az",
    "Basque (巴斯克语)": "eu",
    "Belarusian (白俄罗斯语)": "be",
    "Bengali (孟加拉语)": "bn",
    "Bosnian (波斯尼亚语)": "bs",
    "Bulgarian (保加利亚语)": "bg",
    "Catalan (加泰罗尼亚语)": "ca",
    "Schinese (简体中文)": "zh-CN",
    "Tchinese (繁体中文)": "zh-TW",
    "Croatian (克罗地亚语)": "hr",
    "Czech (捷克语)": "cs",
    "Danish (丹麦语)": "da",
    "Dutch (荷兰语": "nl",
    "English (英语)": "en",
    "Esperanto (世界语)": "eo",
    "Finnish (芬兰语)": "fi",
    "French (法语)": "fr",
    "German (德语)": "de",
    "Greek (希腊语)": "el",
    "Hebrew (希伯来语)": "iw",
    "Hungarian (匈牙利)": "hu",
    "Icelandic (冰岛语)": "is",
    "Indonesian (印度尼西亚语)": "id",
    "Irish (爱尔兰语)": "ga",
    "Italian (意大利语)": "it",
    "Japanese (日语)": "ja",
    "Javanese (爪哇语)": "jw",
    "Kazakh (哈萨克语)": "kk",
    "Khmer (高棉语)": "km",
    "Korean (朝鲜语)": "ko",
    "Lao (老挝语)": "lo",
    "Latin (拉丁语)": "la",
    "Latvian (拉脱维亚语)": "lv",
    "Malay (马来语)": "ms",
    "Maltese (马耳他语)": "mt",
    "Maori (毛利语)": "mi",
    "Nepali (尼泊尔语)": "ne",
    "Norwegian (挪威语)": "no",
    "Persian (波斯语)": "fa",
    "Portuguese (葡萄牙语)": "pt",
    "Romanian (罗马尼亚语)": "ro",
    "Russian (俄语)": "ru",
    "Serbian (塞尔维亚语)": "sr",
    "Slovak (斯洛伐克语)": "sk",
    "Slovenian (斯洛文尼亚语)": "sl",
    "Spanish (西班牙语)": "es",
    "Swedish (瑞典语)": "sv",
    "Thai (泰语)": "th",
    "Turkish (土耳其语)": "tr",
    "Ukrainian (乌克兰语)": "uk",
    "Uzbek (乌兹别克语)": "uz",
    "Vietnamese (越南语)": "vi",
    "Zulu (祖鲁语)": "zu",
}

LANG = [i[1] for i in PBMT.items()]

RequestJson = namedtuple('RequestJson', ['text', 'target'])


class Translation(object):

    def __init__(self, token):
        self.__token = token
        self.__baseURL = "https://translation.googleapis.com/language/translate/v2"
        self.__url = ""
        self.__response = None
        self.__data = None
        self.__translatedText = ""

    def buildURL(self, target, text):
        self.__url = self.__baseURL
        self.__url += "?key={0}&".format(self.__token)
        self.__url += "target={0}&".format(target)
        self.__url += "format=text&"
        self.__url += "q={0}&".format(text)

    def __sendRequest(self, text, target):
        self.buildURL(target, text)
        try:
            self.__response = requests.get(self.__url, timeout=5)
        except Exception as e:
            raise e

    def __checkLang(self, target):
        return target in LANG

    def translate(self, text, target):
        if not self.__checkLang(target):
            return [403, 'The target language is incorrect. For supported languages, please refer to http://35.194.97.99:81/support/languages ']
        try:
            self.__sendRequest(text, target)
        except Exception:
            return [500, "Server Error. "]
        response_code = self.__response.status_code
        response_data = self.__response.text
        self.__data = json.loads(response_data)
        if response_code == 200:
            self.__translatedText = self.__data['data']['translations'][0]['translatedText']
        else:
            self.__translatedText = self.__data['error']['message']
        return [response_code, self.__translatedText]
