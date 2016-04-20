from flask import Flask, request, jsonify
import heapq

app = Flask(__name__)

word_suggestions = {}

@app.route('/suggestion')
def suggestion():
    if 'q' not in request.args:
        return 500
    query = request.args['q']
    context = request.args['c']

    if context not in word_suggestions:
        return jsonify({'suggestions': []})
    else:
        count = len(word_suggestions[context])
        sorted_suggestions = heapq.nlargest(count, word_suggestions[context])
        suggestions = []
        for count, word in sorted_suggestions:
            if word.startswith(query):
                suggestions.append(word)

    return jsonify({'suggestions': suggestions})


if __name__ == '__main__':
    # load autocomplete
    with open('kb/1.txt', 'r') as f:
        current_gram = ''
        for line in f:
            if not line.startswith('\t'):
                current_gram = line.strip()
                word_suggestions[current_gram] = []
            else:
                word, count = line.strip().split(':')
                heapq.heappush(word_suggestions[current_gram], (int(count), word))

    app.run(port=8080)