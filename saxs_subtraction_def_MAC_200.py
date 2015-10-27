import math,os


def saxs_subtraction(file_mostra="",file_buffer="",concentration = 1.0):
    
    #print file_mostra
    #print file_buffer
    

    name_of_sample = file_mostra.split("img_")[1].split("_")[0]
    number_of_sample = file_mostra.split("img_")[1].split("_")[0]
    number_of_sample = file_mostra.split(".dat")[0].split("_")[-1]
    #print "number of sample"
    #print number_of_sample

    path_of_sample=file_mostra.split("/")
    


    if len(path_of_sample)>2:
        print "problem with multi path!!! "
    

    path_of_sample=path_of_sample[0]+"/"

    name_of_buffer = file_buffer.split("img_")[1].split("_")[0]
    
    try:
        int(number_of_sample)
        

    except:
        print"PROBLEM %s is not a natural number"%number_of_sample

    lines_buffer = open(file_buffer).readlines()
    lines_mostra = open(file_mostra).readlines()

    q_buffer = []
    Column_buffer = []
    Error_buffer = []
    q_mostra = []
    Column_mostra = []
    Error_mostra = []
    Column_mostra_buffer = []
    Error_mostra_buffer = []


    k = 0

    for line in lines_buffer:
      #if "q(1/A)" in lines_buffer[k]:
      if "Sample:" in lines_buffer[k]:
        start = k
        #print start
        
      if "creator: radaver" in lines_buffer[k]:
          end = k
          break
      k = k+1
    #print lines_buffer
    lines_buffer = lines_buffer[start+1:end]

    k=0

    for line in lines_mostra:
      if "q(1/A)" in lines_mostra[k]:
        start = k

      if "creator: radaver" in lines_mostra:
          end = k
          break
      k = k+1
      
      
    lines_mostra = lines_mostra[start+1:end]
    #print start
    #print end
    #print lines_buffer

    k = 0
    for line in lines_buffer:
      #print lines_buffer[k].split("  ")  
      q_buffer.append(lines_buffer[k].split("  ")[1])
      #print lines_buffer[k]
      Column_buffer.append(lines_buffer[k].split("  ")[2])
      Error_buffer.append(lines_buffer[k].split("  ")[3].split("\n")[0])
      k=k+1
    k = 0
    for line in lines_mostra:
      q_mostra.append(lines_mostra[k].split("  ")[1])
      Column_mostra.append(lines_mostra[k].split("  ")[2])
      Error_mostra.append(lines_mostra[k].split("  ")[3].split("\n")[0])
      k = k+1

    # Q consistency verification
    k = 0
    
    
    if len(q_buffer) == len(q_mostra):
      if q_buffer[k] != q_mostra[k]:
        print "Error. Different q ranges"
        print "position %i"%k
        k = k+1

    else:
      print "ERROR: Different numer of qs"

    # SUBSTRACTION

    if len(Column_buffer) == len(Column_mostra):
      k = 0
      for i in Column_buffer:
        Column_mostra_buffer.append((float(Column_mostra[k])-float(Column_buffer[k]))/concentration)
        k = k + 1

    
      #print "ERROR: Number of points for mostra is different than number of points for buffer"

    # Error propagation
    
    if len(Error_buffer) == len(Error_mostra):
      k=0
      for i in Error_mostra: 
        Error_mostra_buffer.append(math.sqrt(float(Error_mostra[k])*float(Error_mostra[k]) + float(Error_buffer[k])*float(Error_buffer[k])))
        k = k+1

    folder_subtraction="Rg_%s"%name_of_sample
    
    current_directory=os.getcwd()

    path_of_sample = "%s/%s"%(os.getcwd(),path_of_sample.split("/")[0])
    #print path_of_sample

    
    if os.path.exists(path_of_sample):
        #os.chdir(path_of_sample)
        if not os.path.exists(folder_subtraction):
            os.system("mkdir %s"%(folder_subtraction))
        if not os.path.exists(folder_subtraction):
            print "PROBLEM! Folder not created!"
            
        if len(number_of_sample)==1:
            number_of_sample="0"+number_of_sample
        
        subtracted_file = open("%s/subtracted_%s_minus_%s_%s.dat"%(folder_subtraction,name_of_sample,name_of_buffer,number_of_sample),"w")
        #print "here"
        #print number_of_sample

    else:
        print"could not access:"
        print path_of_sample

    k = 0
    for i in q_buffer:
        #new_lines_subtracted.append("%s\t%s  \t%s\n"%(q_buffer[k],Column_mostra_buffer[k],Error_mostra_buffer[k]))
      if k == 0:
        subtracted_file.write("# file buffer: %s subtracted from file sample: %s\n"%(file_buffer,file_mostra))
        subtracted_file.write("# q(1/A)      \tColumn      \tError       \t\n")
      subtracted_file.write("%s\t%s  \t%s\n"%(q_buffer[k],Column_mostra_buffer[k],Error_mostra_buffer[k]))
      k = k + 1

    subtracted_file.close()
    os.chdir(current_directory)


if __name__ == '__main__':
  import sys
  saxs_subtraction()
