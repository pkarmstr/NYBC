package org.bikher.yiddish;

import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Set;
import java.util.HashSet;

/**
 * A "heavy" stemmer for the Yiddish language. It adjusts for vowel changes by 
 * reducing all yuds to vavs, all alephs to ayins, all tsvey yudn to vav yud. 
 * It also contains a list of nominal and adjectival suffixes which will be removed. 
 * If a token is less than 3 characters, it skips the stemming. 
 * 
 * This algorithm is adapted from the one used in the German stemmer in Lucene. 
 *
 * Created by Keelan Armstrong on 3/12/14.
 */
public class YiddishStemmer {
	
	/**
	 * StringBuilder to hold the string as we modify it
	 */
	private StringBuilder sb = new StringBuilder();
	
	private static final Pattern stemmable;
	private static final Set<String> removableSuffixes;
	static {
		stemmable = Pattern.compile("\\p{InHebrew}{3,}", Pattern.UNICODE_CASE);
		
		removableSuffixes = new HashSet<String>();
		removableSuffixes.add("ער");
		removableSuffixes.add("ן");
		removableSuffixes.add("עם");
		removableSuffixes.add("ען");
		removableSuffixes.add("ע");
		removableSuffixes.add("ס");
		removableSuffixes.add("עס");
		removableSuffixes.add("ות");
		removableSuffixes.add("ים");
		removableSuffixes.add("ה");
		removableSuffixes.add("ל");
	}
	
	/**
	 * Performs the stemming algorithm on a token which has had diacritics
	 * removed and characters normalized
	 * 
	 * @param term a Yiddish word/token
	 * @return the stemmed token
	 */
	public String stem (String term) {
		if (!isStemmable(term)) {
			return term;
		}
		//reset the buffer
	    sb.delete(0, sb.length());
	    sb.insert(0, term);
	    //onto the main attraction
	    strip(sb);
	    substitute(sb);
	    return sb.toString();
	}
	
	/**
	 * Checks if a word is 3 or more characters long and in the Hebrew
	 * script. Uses a regular expression to accomplish this. 
	 * 
	 * @param s the Yiddish word/token
	 * @return a Matcher object which can be treated as a boolean
	 */
	private boolean isStemmable(String s) {
		Matcher m = stemmable.matcher(s);
		return m.matches();
	}
	
	/**
	 * This method naively corrects for umlaut vowel changes in Yiddish. 
	 * It mutates the buffer and returns nothing. 
	 * @param buffer the token
	 */
	private void substitute (StringBuilder buffer) {
		for (int c = 0; c < buffer.length()-1; c++) {
			if (buffer.charAt(c) == 'י') {
				buffer.setCharAt(c, 'ו');
				if (buffer.charAt(c+1) == 'י') {
					c++;
				}
			} else if (buffer.charAt(c) == 'ע') {
				buffer.setCharAt(c, 'א');
			}
		}
	}
	
	/**
	 * Removes the common suffixes found on nouns and adjectives. It does this 
	 * until there are no more possible suffixes at the end of a word or the word's
	 * length drops below 4 characters
	 * 
	 * @param buffer the token, which gets mutated
	 */
	private void strip(StringBuilder buffer) {
		boolean doMore = true;
		while (doMore && buffer.length() > 3) {
			String lastTwoChars = buffer.substring(buffer.length()-2, buffer.length());
			String lastChar = buffer.substring(buffer.length()-1, buffer.length());
			if (removableSuffixes.contains(lastTwoChars)) {
				buffer.delete(buffer.length() - 2, buffer.length());
			}
			else if (removableSuffixes.contains(lastChar)) {
				buffer.delete(buffer.length()-1, buffer.length());
			}
			else {
				doMore = false;
			}
		}
	}
	
	public static void main(String[] args) {
		YiddishStemmer ys = new YiddishStemmer();
		System.out.println(ys.stem("הייזער"));
		System.out.println(ys.stem("קעצל"));
	}
}