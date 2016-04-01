# https://jobs.vector.com/hr_index_de.html

#include <iostream>​​
#include <jobs_vector.h>​​
int main()​​
	{​​
		int myJob = -1;​​
		std::cout<< "Ist es noch Arbeit, ";​​
		std::cout<< "wenn es Spaß macht?";​​
		myJob = jobCode(1,0);​​
		return myJob;​​
	}​​
	
---

using System;​​
​​
public static class Jobs​​
	{​​
		public static void Main(string[] args)​​
			{​​
				Console.WriteLine("Mache einen der besten Arbeitgeber ");​​
				Console.WriteLine("noch eine Idee besser.");​​
				VectorJobs.ShowJobDetails("myJob");​​
			}​​
	}​​

---

using System;​​
​​
public static class Jobs​​
	{​​
		public static void Main(string[] args)​​
			{​​
				Console.WriteLine("Arbeite nicht für einen Automobilkonzern. ");​​
				Console.WriteLine("Arbeite für alle.");​​
				VectorJobs.ShowJobDetails("myJob");​​
			}​​
	}​​