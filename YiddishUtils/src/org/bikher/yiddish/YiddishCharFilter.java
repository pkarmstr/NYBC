package org.bikher.yiddish;

public class YiddishCharFilter {
	
	static final String diacriticsPattern = "[\u05B0\u05B1\u05B2\u05B3\u05B4\u05B5" +
			"\u05B6\u05B7\u05B8\u05B9\u05BC\u05BB\u05BC\u05BD\u05BF\u05B0\u05C1" +
			"\u05C2\u05C4]";
	
	public static String removeDiacritics(String input) {
		return input.replaceAll(diacriticsPattern, "");
	}
	
	public static void main(String[] args) {
		String s = "רבּי";
		System.out.println(s);
		s = removeDiacritics(s);
		System.out.println(s);
	}
}
