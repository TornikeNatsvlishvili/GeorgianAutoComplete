from flask import Flask, request, jsonify
import heapq
import logging
import trie

server = Flask(__name__, static_url_path='')

LOGGING_FILE_NAME = 'log.txt'
NUM_SUGGESTIONS_TO_RETURN = 10
single_word_trie = None

def init():
    global single_word_trie
    logging.basicConfig(filename=LOGGING_FILE_NAME, level=logging.DEBUG)

    print("initializing word store...")
    # load autocomplete
    single_word_trie = trie.load_kb("0.txt")
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
        candidates = single_word_trie.get_all_data_with_prefix(query)
        sorted_candidates = sorted(candidates, key = lambda word: word[1], reverse=True)[:NUM_SUGGESTIONS_TO_RETURN]
        suggestions = [word for word, count in sorted_candidates]
    else:
        pass
        # count = len(word_suggestions['1.txt'][context])
        # sorted_suggestions = heapq.nlargest(count, word_suggestions['1.txt'][context])
        # suggestions = []
        # for count, word in sorted_suggestions:
        #     if word.startswith(query):
        #         suggestions.append(word)

    return jsonify({'suggestions': suggestions[:NUM_SUGGESTIONS_TO_RETURN]})

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8080)