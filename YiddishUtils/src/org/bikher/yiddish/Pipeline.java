package org.bikher.yiddish;

import java.io.FileWriter;
import java.io.IOException;
import java.io.BufferedWriter;
import java.io.File;
import java.util.Scanner;
import java.util.List;
import java.util.LinkedList;
import java.io.Writer;

public class Pipeline {
	
	public static void main(String[] args) throws IOException {
		if (args.length != 2) {
			System.out.println("Usage: Pipeline inputDir outputDir");
			return;
		}
		File inputDir = new File(args[0]);
		String outputDir = args[1];
		
		File[] allFiles = inputDir.listFiles();
		
		
		for (File inputFile : allFiles) {
			
			
			List<String> allParagraphs = new LinkedList<String>();
			String paragraph = "";
			
			Scanner inputStream = new Scanner(inputFile);
			while (inputStream.hasNextLine()) {
				String line = inputStream.nextLine();
				if (line.isEmpty()) {
					allParagraphs.add(paragraph);
					paragraph = "";
				} else {
					paragraph += line;
				}
			}
			
			if (!paragraph.isEmpty()) {
				allParagraphs.add(paragraph); // just in case
			}
			
			String outputFile = outputDir + "/" + inputFile.getName();
			
			Writer destination = new BufferedWriter(new FileWriter(outputFile));
			
			try{
				for (String p : allParagraphs) {
					List<List<String>> tokenizedParagraph = YiddishTokenizer.tokenize(p);
					if (tokenizedParagraph != null) {
						for (List<String> sentence : tokenizedParagraph) {
							for (String word : sentence) {
								destination.write(String.format("%s ", word));
							}
							destination.write("\n");
						}
						destination.write("#\n");
					}
				}
			}
			finally {
				destination.close();
			}
			System.out.println("Wrote your new file: " + outputFile);
			
		}
	}
}
