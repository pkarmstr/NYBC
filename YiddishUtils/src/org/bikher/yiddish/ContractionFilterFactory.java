package org.bikher.yiddish;

import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.util.TokenFilterFactory;

/**
 * Boilerplate for Apache Solr
 * 
 * @author keelan
 *
 */
public class ContractionFilterFactory extends TokenFilterFactory{

	  @Override
	  public TokenStream create(TokenStream input) {
	    return new ContractionFilter(input);
	  }
}