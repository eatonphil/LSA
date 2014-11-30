import os
import shutil

import analyze

TEST_DIR = 'tests/'

def test(path=TEST_DIR):
	for circ in os.listdir(path):
		if circ.endswith('.circ'):
			analyze.analyze(path+circ)
			for lsa in os.listdir('./'):
				if lsa.endswith(analyze.LSA_FORMAT):
					shutil.move(lsa, path+circ[:-5]+'-'+lsa)
		if os.path.isdir(path+circ):
			test(path+circ+'/')

if __name__ == '__main__':
	test()
