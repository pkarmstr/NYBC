import codecs

def get_longest(f, d):
	with codecs.open(f, "r", "UTF-8") as yid_file:
		yiddish = yid_file.read().split("\n\n\n\n")
		s = sorted(yiddish, key=len, reverse=True)
		return s[:d+10]
		
if __name__ == "__main__":
	l = get_longest("wiki_raw_yiddish_corpus.txt", 100)
	useful = []
	for article in l:
		print article
		is_good = raw_input("Is it good?")
		if is_good.startswith("y"):
			useful.append(article)
	with codecs.open("testing_yiddish_corpus.csv", "w", "UTF-8") as y:
		y.write("\n\n\n\n".join(useful))
		
