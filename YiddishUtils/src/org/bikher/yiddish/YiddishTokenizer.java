package org.bikher.yiddish;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class YiddishTokenizer {
	
	public static List<List<String>> tokenize(String input) {
		if (input.isEmpty()) {
			return null;
		}
		input = YiddishCharFilter.removeDiacritics(input);
		String[] sentences = sentenceTokenize(input);
		return wordTokenize(sentences);
	}
	
	public static String[] sentenceTokenize(String input) {
		input = input.replaceAll("([\\.!?])", " $1 ||||");
		return input.split("\\|\\|\\|\\|");
	}

	public static List<List<String>> wordTokenize(String[] sentences) {
		List<List<String>> fullyTokenized = new ArrayList<List<String>>();
		for (String s : sentences) {
			List<String> words = Arrays.asList(s.split(" "));
			List<String> splitted = splitWords(words);
			fullyTokenized.add(splitted);
		}
		return fullyTokenized;
	}
	
	public static List<String> splitWords(List<String> words) {
		List<String> splitted = new ArrayList<String>();
		
		for (String w : words) {
			String[] expanded = expandContraction(w);
			for (int i = 0; i < expanded.length-1; i++) {
				splitted.add(expanded[i]);
			}
			expanded = expandPunctuation(expanded[expanded.length-1]);
			splitted.addAll(Arrays.asList(expanded));
		}
		
		return splitted;
	}
	
	public static String[] expandPunctuation(String word) {
		if (word.length() < 2) {
			return new String[]{word};
		}
		
		if (word.charAt(0) == '„' || word.charAt(0) == '\"') {
			word = word.substring(0, 1) + " " + word.substring(1);
		}
		
		
		
		if (word.indexOf("\"") != -1) {
			word = word.replace("\"", " \"");
		}
		
		if (word.indexOf(",") != -1) {
			word = word.replace(",", " ,");
		}
		
		if (word.indexOf(":") != -1) {
			word = word.replace(":", " :");
		}
		
		if (word.indexOf("-") != -1) {
			word = word.replace("-", " - ");
		}
		
		if (word.indexOf("(") != -1) {
			word = word.replace("(", "( ");
		}
		
		if (word.indexOf(")") != -1) {
			word = word.replace(")", " )");
		}
		
		return word.split(" ");
	}
	
	public static String[] expandContraction(String word) {
		if (word.indexOf("'") != -1) {
			if (word.matches("\\w{1,2}'\\w+")) {
				return word.replace("'", "' ").split(" ");
			}
			else if (word.matches("\\w+?'\\w{1,2}")) {
				return word.replace("'", " '").split(" ");
			}
			else {
				return new String[]{word};
			}
		} 
		else {
			return new String[]{word};
		}
	}
	
	public static void main(String[] args) {
		String input = "דער רבּי האט מיך געלערענט," +
				" אַז איך (זאל) ניט קלערען און ניט פרעגען . וואס גאטט" +
				" טהוט פערשטעהט ניט אַ מענש , מן-הסתּם האט אַזוי בּעדארפט" +
				" צוא זיין איך זאל בּלייבּען אַ יתום . „ד' נתן יד' לקח" +
				" , יהי שם ד' מבורך- , גאט גיט איינעם עלטערען" +
				" , נעהמט זייא אוועק , זאל גאט'ס נאמען\"" +
				" זיין געלויבּט , ווייל ער איז דער שופט צדק . ";
		
		List<List<String>> t = tokenize(input);
		for (List<String> ls : t) {
			for (String s : ls) {
				System.out.println(s);
			}
			System.out.println();
		}
	}
}
