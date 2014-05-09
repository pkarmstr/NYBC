package org.bikher.yiddish;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Pipeline {
	
	public static void main(String[] args) throws IOException {
		if (args.length != 3) {
			System.out.println("Usage: Pipeline inputFile outputFile");
			return;
		}
		String inputFile = args[1];
	}
}
