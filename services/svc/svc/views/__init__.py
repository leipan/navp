import sys, os
cwd = os.getcwd()
sys.path.append(cwd+'/svc/views/')
print (sys.path)
import main
