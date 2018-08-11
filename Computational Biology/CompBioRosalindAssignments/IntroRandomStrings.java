import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class IntroRandomStrings {

	String dnaSequence;
	ArrayList<Double> probabilities = new ArrayList<Double>();
	public void readFile(String path)
	{
		try {
			File file = new File(path);
			Scanner scanner = new Scanner(file);
			dnaSequence = scanner.next().toString();
			//System.out.print(dnaSequence);
			while(scanner.hasNextDouble())
			{
				Double prob = scanner.nextDouble();
				probabilities.add(prob);
			}
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public void probForGivenDNA()
	{
		Double gcProb;
		Double atProb;
		for(int i = 0;i < probabilities.size(); ++i )
		{
			Double finalProb = 0.0;
			gcProb = probabilities.get(i)/2.0;
			atProb = (1.0 - probabilities.get(i))/2.0;
			gcProb = Math.log10(gcProb);
			atProb = Math.log10(atProb);
			for(int str_index=0; str_index<dnaSequence.length(); ++ str_index)
			{
				if(dnaSequence.charAt(str_index) == 'C' || dnaSequence.charAt(str_index) == 'G')
				{
					finalProb += gcProb;
				}else {
					finalProb += atProb;
				}
			}
			System.out.print(String.format("%.3f",finalProb)   +" ");
		}
	}
	
	
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		IntroRandomStrings graph = new IntroRandomStrings();
		graph.readFile("/Users/jatingarg/Downloads/rosalind_prob.txt");
		graph.probForGivenDNA();
	}

}
