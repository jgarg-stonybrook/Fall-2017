import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class GenomeAssembly {

	ArrayList<StringBuilder> strlist = new ArrayList<StringBuilder>();
	public void readFile(String path)
	{
		try {
			File file = new File(path);
			Scanner scanner = new Scanner(file);
			StringBuilder value = new StringBuilder("");
			int flag = 0;
			while(scanner.hasNext() == true)
			{
				String line = scanner.next();
				if(line.startsWith(">") == false && flag == 1)
				{
					value.append(line);
				}else {
					if(flag == 1)
					{
						strlist.add(value);
						value = new StringBuilder("");
						flag = 1;
						continue;
					}
					flag =1;
				}
				
			}
			strlist.add(value);
			scanner.close();
			//System.out.println(strlist);
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public String supercs()
	{
		for(int count = 0;count<=strlist.size(); ++count)
		{
			int max = -1,pre = -1, suf = -1;
			int index1=0;
			int index2=0;
			StringBuilder str1 = new StringBuilder(""),str2 = new StringBuilder("");
			for(int first_index = 0; first_index<strlist.size()-1; ++first_index)
			{
			for(int second_index = first_index+1; second_index<strlist.size(); ++second_index)
			{
					str1 = strlist.get(first_index);
					str2 = strlist.get(second_index);
					int overlap1 =  isMatches(str1,str2);
					int overlap2 = isMatches(str2,str1);
					if(overlap1>max && overlap1 >= overlap2)
					{
						pre = overlap1;
						index1 = first_index;
						index2 = second_index;
						max = pre;
					}
					if(overlap2>max && overlap2 > overlap1)
					{
						suf = overlap2;
						index1 = second_index;
						index2 = first_index;
						max = suf;
					}					
			}
			}
			StringBuilder str = new StringBuilder("");
			if(max != -1)
			{
				str1 = strlist.get(index1);
				str2 = strlist.get(index2);
				//if(pre >= suf)
				//{
					str = str1.append(str2.substring(max,str2.length()));
				//}else {
					//str = str2.append(str1.substring(suf,str1.length()));
				//}
			}
			strlist.set(index1, str);
			strlist.remove(index2);
		}
		return strlist.get(0).toString();
	}
	
	public int isMatches(StringBuilder str1,StringBuilder str2)
	{
		int leng1 = str1.length();
		int leng2 = str2.length();
		int length = leng1 < leng2 ? leng1 : leng2;
		int max = -1;
		for(int i = 1; i<length; ++i)
		{
			if(str1.substring(leng1-i,leng1).equals(str2.substring(0,i)))
			{
				
				if(i > max)
				{
					max = i;
				}
			}
		}
		return max;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		GenomeAssembly genas = new GenomeAssembly();
		genas.readFile("/Users/jatingarg/Downloads/rosalind_long (5).txt");
		System.out.println(genas.supercs());
	}

}
