import subprocess
import sys
class libloader:
    def install_packages(self,name):
        subprocess.call([sys.executable, '-m', 'pip', 'install', name , '-q'])
    def __init__(self):
        libs = ['numpy' , 'pandas' , 'matplotlib' , 'scikit-learn','python-dotenv']
        for lib in libs:
            print("Installing " + lib)
            self.install_packages(lib)
        
libloader()