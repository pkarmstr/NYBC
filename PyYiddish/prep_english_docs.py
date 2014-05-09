__author__ = 'keelan'

import sys
import nltk
import os
import cStringIO

def nested_tokenize(untokenized_sentences):
    tokenized_sents = nltk.sent_tokenize(untokenized_sentences)
    tokenized_words = [nltk.word_tokenize(sent) for sent in tokenized_sents]
    return tokenized_words

input_dir = sys.argv[1]
output_dir = sys.argv[2]

book = []

for f in os.listdir(input_dir):
    with open(os.path.join(input_dir, f), "r") as f_in:
        book = []
        paragraph = []
        for line in f_in:
            line = line.rstrip().strip()
            if line == "":
                book.append(" ".join(paragraph))
                paragraph = []
            else:
                paragraph.append(line)

    output_buffer = cStringIO.StringIO()
    for paragraph in book:
        tokenized_paragraph = nested_tokenize(paragraph)
        if len(tokenized_paragraph) > 0:
            for sentence in tokenized_paragraph:
                if len(sentence) > 0:
                    output_buffer.write("{:s}\n".format(" ".join(sentence)))
            output_buffer.write("#\n")

    with open(os.path.join(output_dir, f), "w") as f_out:
        f_out.write(output_buffer.getvalue())

    output_buffer.close()
    print "wrote to", os.path.join(output_dir, f)