package org.bikher.yiddish;

import java.io.IOException;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.KeywordAttribute;

public class YiddishStemFilter extends TokenFilter {
	
	private YiddishStemmer stemmer = new YiddishStemmer();
	private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
	private final KeywordAttribute keywordAttr = addAttribute(KeywordAttribute.class);
	
	public YiddishStemFilter(TokenStream in) {
		super(in);
	}
	
	/**
     * @return  Returns true for next token in the stream, or false at EOS
     */
    @Override
    public boolean incrementToken() throws IOException {
      if (input.incrementToken()) {
        String term = termAtt.toString();

        if (!keywordAttr.isKeyword()) {
          String s = stemmer.stem(term);
          // If not stemmed, don't waste the time adjusting the token.
          if ((s != null) && !s.equals(term))
            termAtt.setEmpty().append(s);
        }
        return true;
      } else {
        return false;
      }
    }
}

