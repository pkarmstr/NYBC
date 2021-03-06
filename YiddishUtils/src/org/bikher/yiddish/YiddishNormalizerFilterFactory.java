package org.bikher.yiddish;

import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.util.TokenFilterFactory;

/**
 * boilerplate for Apache Solr
 * 
 * @author keelan
 *
 */
public class YiddishNormalizerFilterFactory extends TokenFilterFactory {

	@Override
	public TokenStream create(TokenStream arg0) {
		return new YiddishNormalizerFilter(arg0);
	}

}
