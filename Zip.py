import gzip 
import tarfile
with gzip.open(r"C:\Users\s-coughlinz\Downloads\PyYAML-5.3.1.tar.gz","rb") as source:
	with open(r"C:\Users\s-coughlinz\Downloads\PyYAML-5.3.1.tar","wb") as out:
		out.write(source.read())
with tarfile.open(r"C:\Users\s-coughlinz\Downloads\PyYAML-5.3.1.tar","r") as t:
    t.extractall(r"C:\Users\s-coughlinz\Downloads\PyYAML-5.3.1")
    
    
    
    
    
    