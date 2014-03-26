package org.apache.lucene.analysis.yi;

import java.util.Locale;
import java.util.regex.*;
import java.util.Map;
import java.util.HashMap;

/**
 * A stemmer for Yiddish language
 *
 * Created by keelan on 3/12/14.
 */
public class YiddishStemmer {
	
	/**
	 * StringBuilder to hold the string as we modify it
	 */
	private StringBuilder sb = new StringBuilder();
	
	/**
	 * counts substitutions that are made throughout the process
	 */
	private int substCount = 0;
	
	private static final Pattern stemmable;
	private static final Map<Character, Character> finalLetters;
	static {
		stemmable = Pattern.compile("\\p{InHebrew}{3,}", Pattern.UNICODE_CASE);
		finalLetters = new HashMap<Character, Character>();
		finalLetters.put('י', 'ו');
		finalLetters.put('ע', 'א');
		finalLetters.put('ן', 'נ');
		finalLetters.put('ם', 'מ');
		finalLetters.put('ך', 'כ');
		finalLetters.put('ף', 'פ');
		finalLetters.put('ץ', 'צ');
	}
	
	protected String stem (String term) {
		if (!isStemmable(term)) {
			return term;
		}
		//reset the buffer
	    sb.delete(0, sb.length());
	    sb.insert(0, term);
	    //onto the main attraction
	}
	
	private boolean isStemmable(String s) {
		Matcher m = stemmable.matcher(s);
		return m.matches();
	}
	
	private void substitute (StringBuilder buffer) {
		substCount = 0;
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
		char lastChar = buffer.charAt(buffer.length()-1);
		if (finalLetters.containsKey(lastChar)) {
			buffer.setCharAt(buffer.length()-1, finalLetters.get(lastChar));
		}
	}
	
	public static void main(String[] args) {
		YiddishStemmer ys = new YiddishStemmer();
		StringBuilder sb = new StringBuilder("הייזער");
		ys.substitute(sb);
		System.out.println(sb);
	}
}
