package org.bikher.yiddish;

import java.util.HashMap;
import java.util.Map;

public class YiddishNormalizer {

	private static final Map<Character, Character> charNormalizationMap;
	private static final String diacritics = "([\u05B0\u05B1\u05B2\u05B3\u05B4" +
			"\u05B5\u05B6\u05B7\u05B8\u05B9\u05BC\u05BB\u05BC\u05BD\u05BF\u05B0" +
			"\u05C1\u05C2\u05C4])";
	static {
		charNormalizationMap = new HashMap<Character, Character>();
		charNormalizationMap.put('ן', 'נ');
		charNormalizationMap.put('ם', 'מ');
		charNormalizationMap.put('ך', 'כ');
		charNormalizationMap.put('ף', 'פ');
		charNormalizationMap.put('ץ', 'צ');
	}
	
	public static String normalize(String s) {
		s = s.replaceAll(diacritics, "");
		char lastChar = s.charAt(s.length()-1);
		if (charNormalizationMap.containsKey(lastChar)) {
			s = s.substring(0, s.length()-2) + charNormalizationMap.get(lastChar);
		}
		return s;
	}
}
