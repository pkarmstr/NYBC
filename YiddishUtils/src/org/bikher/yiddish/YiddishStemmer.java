package org.bikher.yiddish;

import java.util.regex.*;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;

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
	
	private static final Pattern stemmable;
	private static final Map<Character, Character> charNormalizationMap;
	private static final Set<String> suffixes;
	static {
		stemmable = Pattern.compile("\\p{InHebrew}{3,}", Pattern.UNICODE_CASE);
		charNormalizationMap = new HashMap<Character, Character>();
		charNormalizationMap.put('ן', 'נ');
		charNormalizationMap.put('ם', 'מ');
		charNormalizationMap.put('ך', 'כ');
		charNormalizationMap.put('ף', 'פ');
		charNormalizationMap.put('ץ', 'צ');
		
		suffixes = new HashSet<String>();
		suffixes.add("ער");
		suffixes.add("ן");
		suffixes.add("עם");
		suffixes.add("ען");
		suffixes.add("ע");
		suffixes.add("ס");
		suffixes.add("עס");
		suffixes.add("ות");
		suffixes.add("ים");
	}
	
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
	
	private boolean isStemmable(String s) {
		Matcher m = stemmable.matcher(s);
		return m.matches();
	}
	
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
		char lastChar = buffer.charAt(buffer.length()-1);
		if (charNormalizationMap.containsKey(lastChar)) {
			buffer.setCharAt(buffer.length()-1, charNormalizationMap.get(lastChar));
		}
	}
	
	private void strip(StringBuilder buffer) {
		boolean doMore = true;
		while (doMore && buffer.length() > 3) {
			String lastTwoChars = buffer.substring(buffer.length()-2, buffer.length());
			String lastChar = buffer.substring(buffer.length()-1, buffer.length());
			if (suffixes.contains(lastTwoChars)) {
				buffer.delete(buffer.length() - 2, buffer.length());
			}
			else if (suffixes.contains(lastChar)) {
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
		System.out.println(ys.stem("קאַץ"));
	}
}