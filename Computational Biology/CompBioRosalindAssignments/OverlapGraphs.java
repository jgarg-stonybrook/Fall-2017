import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.HashMap;

public class OverlapGraphs {

	HashMap<Integer,String> keys = new HashMap<Integer,String>();
	HashMap<Integer,String> values = new HashMap<Integer,String>();
	int count;
	public void readFile(String path)
	{
		try {
			File file = new File(path);
			BufferedReader bufferReader = new BufferedReader(new FileReader(file));
			String line = "";
			line = bufferReader.readLine().trim();
			count = 1;
			while(line != null)
			{
				if(line.startsWith(">"))
				{
					keys.put(count, (line.substring(1)));
					line = bufferReader.readLine();
					if(line != null)
						line = line.trim();
				}else {
					StringBuilder value = new StringBuilder();
					value.append(line);
					line = bufferReader.readLine();
					if(line != null)
						line = line.trim().toString();
					while(line != null && line.startsWith(">") != true)
					{
						value.append(line);
						line = bufferReader.readLine();
						if(line != null)
							line = line.trim().toString();
					}
					values.put(count, value.toString());
					count+=1;
				}
				
			}
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public void drawEdges()
	{
		int k = 3;
		for(int firstIndex = 1; firstIndex < count ; ++firstIndex)
		{
			int length = values.get(firstIndex).length();
			for(int secondIndex = 1; secondIndex<count; ++secondIndex)
			{
				if(firstIndex != secondIndex)
				{
					if(values.get(firstIndex).substring(length-k, length).equals(values.get(secondIndex).substring(0, k)))
					{
						System.out.println(keys.get(firstIndex)+ " " + keys.get(secondIndex));
					}
				}
			}
		}
		
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		OverlapGraphs graph = new OverlapGraphs();
		graph.readFile("/Users/jatingarg/Downloads/rosalind_grph (1).txt");
		graph.drawEdges();
	}

}
