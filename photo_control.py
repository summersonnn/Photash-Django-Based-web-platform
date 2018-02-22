import cv2
import numpy as np
import os
import time
import sys

def dummycheck():
	copy_list=[]
	file = open('check.txt', 'r+')
	d = file.readlines()
	file.seek(0)

	for line in d:
		line = line[:-1]
		lineToCheck = control(line)

	file.truncate()
	file.close()

def are_arrays_equal(a1, a2):
	return np.array_equal(a1, a2)

def control(image_name):
	abs_folder_path = "C:\\Users\\Root\\Desktop\\PhotashBackend\\photopool"
	rel_folder_path = 'photopool'


	for file_name in os.listdir(abs_folder_path):  # itereate through all files in the photopool folder

		# Dosya bulunuyor mu? Daha önceden silinmiş de olabilir. (kopya ise silinmiştir)
		if (os.path.isfile(os.path.join(abs_folder_path, image_name))):
			new_image = cv2.imread(os.path.join(abs_folder_path, image_name))
		else:
			return False

		#Kendisi ile karşılaştırılmaması için geç
		if file_name == image_name:
			continue

		current_image_in_photopool = cv2.imread(os.path.join(abs_folder_path, file_name))

		#İki fotoğrafın karşılaştırılması
		if are_arrays_equal(new_image, current_image_in_photopool):
			#Oluşturulma tarihlerine göre en yakın zamanda oluşturulanı siliyorum. O kopyadır.
			if(time.ctime(os.path.getctime(os.path.join(abs_folder_path, image_name))) > time.ctime(os.path.getctime(os.path.join(abs_folder_path, file_name)))):
				originalfile=file_name
				copyfile = image_name
				os.remove(os.path.join(rel_folder_path, image_name))
			else:
				originalfile = image_name
				copyfile = file_name
				os.remove(os.path.join(rel_folder_path, file_name))

			print("COPY FOUND. Original file: ", originalfile,"\nCopy File: ",copyfile)
			print("Copy file is deleted.")
			return True, file_name

	return False, image_name


dummycheck()



