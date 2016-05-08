from flask import Flask, request, jsonify
import heapq
import logging

server = Flask(__name__, static_url_path='')

LOGGING_FILE_NAME = 'log.txt'
NUM_SUGGESTIONS_TO_RETURN = 10
word_suggestions = {}
single_word_suggestions = []


def load_kb(name):
    word_dict = {}
    with open('kb/{}'.format(name), 'r') as f:
        current_gram = ''
        for line in f:
            if not line.startswith('\t'):
                current_gram = line.strip()
                word_dict[current_gram] = []
            else:
                word, count = line.strip().split(':')
                heapq.heappush(word_dict[current_gram], (int(count), word))
    word_suggestions[name] = word_dict


def init():
    global single_word_suggestions
    logging.basicConfig(filename=LOGGING_FILE_NAME, level=logging.DEBUG)

    print("initializing word store...")
    # load autocomplete
    load_kb("0.txt")
    # for efficiency pre-sort and save all items since there is only one key
    count = len(word_suggestions['0.txt'][''])
    single_word_suggestions = heapq.nlargest(count, word_suggestions['0.txt'][''])

    load_kb("1.txt")
    print("done")


init()

@server.route('/')
def main():
    return server.send_static_file('index.html')

@server.route('/suggestion')
def suggestion():
    if 'q' not in request.args:
        return 500
    query = request.args['q']
    context = request.args.get('c', '')

    if context == '':
        suggestions = []
        for count, word in single_word_suggestions:
            if word.startswith(query):
                suggestions.append(word)
    else:
        count = len(word_suggestions['1.txt'][context])
        sorted_suggestions = heapq.nlargest(count, word_suggestions['1.txt'][context])
        suggestions = []
        for count, word in sorted_suggestions:
            if word.startswith(query):
                suggestions.append(word)

    return jsonify({'suggestions': suggestions[:NUM_SUGGESTIONS_TO_RETURN]})

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8080)