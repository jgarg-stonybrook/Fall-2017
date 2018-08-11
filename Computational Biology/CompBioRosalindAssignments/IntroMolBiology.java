import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class IntroMolBiology {

	String dnaSequence;
	public void readFile(String path)
	{
		try {
			File file = new File(path);
			Scanner scanner = new Scanner(file);
			dnaSequence = scanner.next().toString();
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public void count()
	{
		int a = 0,c = 0,g = 0,t= 0;
		for(int str_index=0; str_index<dnaSequence.length(); ++ str_index)
		{
			if(dnaSequence.charAt(str_index) == 'A')
			{
				a +=1;
			}else if(dnaSequence.charAt(str_index) == 'C')
			{
				c +=1;
			}else if(dnaSequence.charAt(str_index) == 'G')
			{
				g+=1;
			}else {
				t+=1;
			}
		}
		System.out.println(a+" "+c+ " "+ g + " " + t);
			
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		IntroMolBiology irs = new IntroMolBiology();
		irs.readFile("/Users/jatingarg/Downloads/rosalind_dna-1.txt");
		irs.count();
	}

}
