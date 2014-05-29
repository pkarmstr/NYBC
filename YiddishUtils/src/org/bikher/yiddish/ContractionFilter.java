package org.bikher.yiddish;

import java.io.IOException;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.KeywordAttribute;

public class ContractionFilter extends TokenFilter {

	private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
	private final KeywordAttribute keywordAttr = addAttribute(KeywordAttribute.class);
	static final String[] initialContractions = {"כ'", "ס'"};
	static final String[] finalContractions = {"'ן", "'ס"};
	static final String hyphen = "\u05be";
	
	public ContractionFilter(TokenStream in) {
		super(in);
	}
	
	@Override
	public boolean incrementToken() throws IOException {
		if (input.incrementToken()) {
			
			String term = termAtt.toString();
			termAtt.setEmpty();
			if (!keywordAttr.isKeyword()) {
				
				if (term.indexOf('\u05BE') != -1) {
					String[] hyphenatedTerms = term.split("\u05BE");
					for (int i = 0; i < hyphenatedTerms.length-1; i++) {
						termAtt.append(hyphenatedTerms[i]);
					}
					term = hyphenatedTerms[hyphenatedTerms.length-1];
				}
				
				for (String c : initialContractions) {
					if (term.startsWith(c)) {
						termAtt.append(c);
						term = term.substring(2);
						break;
					}
				}
		          
				for (String c : finalContractions) {
					if (term.endsWith(c)) {
						termAtt.append(term.substring(0, term.length()-2));
						termAtt.append(c);
						term = null;
						break;
					}
				}
		          
				// If not stemmed, don't waste the time adjusting the token.
				if (term != null) {
					termAtt.append(term);
				}
			}
		    return true;
		} else {
			return false;
		}
	}
	
	public static void main(String[] args) {
		//TODO
	}
}
