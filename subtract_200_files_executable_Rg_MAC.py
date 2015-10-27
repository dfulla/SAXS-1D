import saxs_subtraction_def_MAC_200 as SS
import os


# under development:
# generalise for other formats

number=raw_input("introduce the three digits (048):\n")
#number='048'
concentration=float(raw_input("concentration, please:\n"))
#concentration=2.0

#name_of_path_sample = "b21-21%s.unsub/b21-21%s_sample_0.dat"%(number,number)
name_of_path_sample = "img_0%s_00001.dat"%(number)

if os.path.isfile(name_of_path_sample):
    pass
else:
    print "file %s not found"%name_of_path_sample

path = "b21-21%s.unsub/"%number
#concentration=4.5

all_files_samples = []
all_files_buffers = []

name_of_sample = name_of_path_sample
name_of_sample_template = name_of_sample.split(".dat")[0].split("_000")[0]+"_"

if len(name_of_sample.split(".dat")[0].split("_000")) == 3:
    name_of_sample_template = '%s_000%s'%(name_of_sample.split(".dat")[0].split("_000")[0],name_of_sample.split(".dat")[0].split("_000")[1])
    
reference_sample_number=name_of_sample_template.split("_")[1]
template_first_part = name_of_sample_template.split("-")[0]
template_last_part = name_of_sample_template.split(reference_sample_number)[1]
reference_buffer_number=int(reference_sample_number)-1
reference_buffer_number='0'+str(reference_buffer_number)

if len(reference_buffer_number) == 2:
    reference_buffer_number = '00%s'%reference_buffer_number

if len(reference_buffer_number) == 3:
    reference_buffer_number = '0'+reference_buffer_number

name_of_buffer_template = 'img_'

number_of_sample = name_of_sample.split(".dat")[0].split("_")[-1]
number_of_files = 190

i=1
while i<number_of_files:
    if i < 100:
        index_file = '000'+str(i)
    if i > 100:
        index_file = '00' + str(i)
    if len(index_file) == 4:
        index_file = '0'+index_file
    
    name_sample = name_of_sample_template+index_file+".dat"
    if len(name_sample.split('_')) == 2:
        name_sample = name_of_sample_template+'_'+index_file+".dat"
    
    if os.path.exists(name_sample):
        all_files_samples.append(name_sample)
        
    i=i+1

i=0
while i<number_of_files:
    if i < 100:
        index_file = '000'+str(i)
    if i >= 100:
        index_file = '00'+str(i)
    
    if len(index_file) == 4:
        index_file = '0'+index_file    
    name_buffer = name_of_buffer_template + reference_buffer_number +'_'+ index_file+".dat"
    
    if os.path.exists(name_buffer):
        all_files_buffers.append(name_buffer)
    i=i+1
    
if len(all_files_samples) ==  len(all_files_buffers):
    i=0
    while i<number_of_files:

        try:
            SS.saxs_subtraction(all_files_samples[i],all_files_buffers[i],concentration)
            print all_files_samples[i],all_files_buffers[i],concentration
            i = i+1
        except:
            i = i+1
            

else:
    print "Number of buffers files is %i and number of sample files is %i. They do not coincide. Modify the paramenter number_of_files"%(len(all_files_samples),len(all_files_buffers))
            
one_path = "%s/Rg_%s"%(os.getcwd(),reference_sample_number)

if os.path.exists(one_path):
    os.chdir(one_path)
    files=os.listdir(one_path)

    results=open("results.txt","w")
    k=0
    files_subtracted=[]

    for file in files:
                if len(files[k].split(".dat"))>1:

                    if "table" not in files[k]:
                        os.system("autorg %s> txt.txt"%files[k])
                        print "autorg %s> txt.txt"%files[k]
                    
                        file_results=open("txt.txt").readlines()
                        files_subtracted.append("%s\t"%(files[k].split("\n")[0]))
                        j=0
                        for i in file_results:
            
                            results.write(file_results[j])
                            j=j+1
                k=k+1
    
    results.close()	

    k=0
    extract_rg=open("results.txt").readlines()
    Rg_table = open("table_rg_%s.txt"%name_of_sample.split("_sample_0.dat")[0],"w")
    Rg_rg=[]
    Rg_line=[]

    Rg_array=[]
    Rg_error_array=[]
    I0_array=[]
    I0_error_array=[]
    Quality_array=[]
    
    for line in extract_rg:
      if len(extract_rg[k].split("Rg   ="))>1:
        Rg_array.append(float(extract_rg[k].split("Rg   =")[1].split("+/-")[0]))
        Rg_error_array.append(float(extract_rg[k].split("Rg   =")[1].split("+/-")[1].split("(")[0].split("\n")[0]))

      if len(extract_rg[k].split("I(0) ="))>1:
        I0_array.append(float(extract_rg[k].split("I(0) =")[1].split("+/-")[0]))
        I0_error_array.append(float(extract_rg[k].split("I(0) =")[1].split("+/-")[1]))
        
      if len(extract_rg[k].split("Quality:"))>1:
        Quality_array.append(float(extract_rg[k].split("Quality:")[1].split("%")[0]))
            
      k=k+1

    k=0

    for line in Rg_array:
      if k==0:
        Rg_table.write("Number of scan\t\t\t\tName of file\t\t\t\tRg\tRg_error\tI(0)\t\tI(0) error\tFidelity\n\n")
      
      lines_for_table="\t%i\t\t%s\t%.2f\t%.2f\t\t%.4f\t\t%.7f\t%.1f\n"%(k,files_subtracted[k],Rg_array[k],Rg_error_array[k],I0_array[k],I0_error_array[k],Quality_array[k])
      
      Rg_table.write(lines_for_table)
      k=k+1
      
    Rg_table.close()

else:

    print "Failed to make Rg tables"
