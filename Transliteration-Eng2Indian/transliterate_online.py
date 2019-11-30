"""
Indian Transliterator:
To transliterate a given English word to Indian language(s) using Online APIs.

Author:	 Gokul NC <gokulnc@ymail.com>
Release: 2019, The MIT License
"""

import requests, json, sys
g_api = 'https://inputtools.google.com/request?text=%s&itc=%s-t-i0-und&num=%d'
qp_api = 'http://xlit.quillpad.in/quillpad_backend2/processWordJSON?lang=%s&inString=%s'

lang2code = {
	'tamil': 'ta',
	'hindi': 'hi',
	'telugu': 'te',
	'marathi': 'mr',
	'punjabi': 'pa',
	'bengali': 'bn',
	'gujarati': 'gu',
	'kannada': 'kn',
	'malayalam': 'ml',
	'nepali': 'ne'
}

def gtransliterate(word, lang_code, num_suggestions=10):
	response = requests.request('GET', g_api % (word, lang_code, num_suggestions), allow_redirects=False, timeout=5)
	r = json.loads(response.text)
	if 'SUCCESS' not in r[0] or response.status_code != 200:
		print('Request failed with status code: %d\nERROR: %s' % (response.status_code, response.text), file=sys.stderr)
		return []
	return r[1][0][1]

def qp_transliterate(word, lang):
	response = requests.request('GET', qp_api % (lang, word), allow_redirects=False, timeout=5)
	if 'Internal Server Error' in response.text or response.status_code != 200:
		print('Request failed with status code: %d\nERROR: %s' % (response.status_code, response.text), file=sys.stderr)
		return []
	r = json.loads(response.text)
	suggestions = r['twords'][0]['options']
	suggestions.append(r['itrans'])
	return suggestions

def transliterate(word, lang, source):
	if 'quill' in source:
		return qp_transliterate(word, lang)
	if 'google' in source:
		return gtransliterate(word, lang2code[lang])
	sys.exit('ERROR: Source %s not found' % source)
	
if __name__ == '__main__':
	word, lang = sys.argv[1:]
	if not word or not lang in lang2code:
		sys.exit('USAGE: python %s <eng_word> <supported_lang>' % sys.argv[0])
	print('QUILLPAD suggestions:\n%s\n' % transliterate(word, lang, 'quillpad'))
	print(' GOOGLE  suggestions:\n%s\n' % transliterate(word, lang, 'google'))
