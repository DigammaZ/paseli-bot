import requests

URL_ENDPOINT = 'http://jisho.org/api/v1/search/words'


def search_jisho(query):
  params = {'keyword': query}
  resp = requests.get(URL_ENDPOINT, params=params)
  try:
    resp.raise_for_status()
    data = resp.json()['data']
    if data:
      return create_output(data)
    else:
      return 'Could not find anything for {0}.'.format(query)
  except requests.exceptions.HTTPError:
    if resp.status_code == 404:
      return 'Jisho appears to be down.'
    else:
      return 'Random ass error: {0}.'.format(resp.status_code)


def create_output(data):
  output = []
  for word_num, word in enumerate(data[:3]):
    word_arr, japanese_arr, japanese = [], [], word['japanese']
    for japanese_word in japanese:
      word_exists = 'word' in japanese_word and japanese_word['word']
      reading_exists = 'reading' in japanese_word and japanese_word['reading']
      if word_exists and reading_exists:
        japanese_arr.append('{0} ({1})'.format(japanese_word['word'], japanese_word['reading']))
      elif word_exists:
        japanese_arr.append(japanese_word['word'])
      else:
        japanese_arr.append(japanese_word['reading'])
    word_arr.append(', '.join(japanese_arr))
    senses = word['senses']

    parts_of_speech = senses[0]['parts_of_speech']
    word_arr.append('_{0}_'.format(', '.join(parts_of_speech)))
    for sense_num, sense in enumerate(senses):
      definitions = sense['english_definitions']
      tags = '_{0}_'.format(', '.join(sense['tags'])) if sense['tags'] else ''
      word_arr.append('**{0}**) {1} {2}'.format(str(sense_num), '; '.join(definitions), tags))
    output.append('\n'.join(word_arr))
  return '\n\n'.join(output)
