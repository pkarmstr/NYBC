package org.bikher.yiddish;

import java.io.IOException;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.KeywordAttribute;

/**
 * boilerplate for Apache Solr
 * 
 * @author keelan
 *
 */
public class YiddishNormalizerFilter extends TokenFilter {
	
	private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
	private final KeywordAttribute keywordAttr = addAttribute(KeywordAttribute.class);
	
	public YiddishNormalizerFilter(TokenStream in) {
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
          String s = YiddishNormalizer.normalize(YiddishDiacriticNormalizer.removeDiacritics(term));
          
          // If not normalized, don't waste the time adjusting the token.
          if ((s != null) && !s.equals(term))
            termAtt.setEmpty().append(s);
        }
        return true;
      } else {
        return false;
      }
    }

}
