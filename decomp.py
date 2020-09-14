import sys

if len(sys.argv) == 3:
    source = sys.argv[1]
    destination = sys.argv[2]
else:
    print("arguments error: this program requires two arguments")
    print("reader -/path/to/source/folder/ -/path/to/destination/folder/")
    exit()

import os
f = []
for root, dirs, files in os.walk(source, topdown=False):
    for name in files:
        f.append(os.path.join(root, name))

print("start decompressing...")

for fileName in f:
    
    try:

        fileIndex = f.index(fileName)
        print(fileName+" "+str(fileIndex+1)+"/"+str(len(f))+" "+str(round((fileIndex+1)*100/len(f),1))+"%")

        #open the file
        file = open(fileName, 'rb')

        #dict to manage keywors_assignment
        keyword_assignment = dict()

        #list to manage object statements
        object_list = []

        #dict to manage pointer statements
        pointer = dict()

        #decode the length of the first record
        length_indicator = int.from_bytes(file.read(2), byteorder='little')

        #convert the record into a utf-8 char string
        record = file.read(length_indicator).decode('utf-8')

        if length_indicator % 2 != 0:
                    file.read(1)

        #read the label of the compressed immage
        while(record[0:3] != 'END'):
            #detect the statement
            if record[0] == '^':
                statement = 'pointer'
            elif record[0:2] == '/*':
                statement = 'comment'
            elif record[0:6] == 'OBJECT':
                statement = 'object'
            elif record[0:2]=='  ':
                statement = 'strange'
            else:
                statement = 'keyword_assignment'

            #decode keyword_assignment and pointer
            if(statement=='keyword_assignment' or statement=='pointer'):
                i = 0
                while(record[i]!=' '):
                    i=i+1
                name = record[0:i]
                while(record[i]!='='):
                    i = i+1 
                value = record[i+2:len(record)] 
                if(statement == 'keyword_assignment'):
                    keyword_assignment[name] = value
                else:
                    pointer[name] = value
            
            #decode object
            if(statement=='object'):
                object_list.append(dict())
                i = 0
                while(record[i]!='='):
                    i = i+1  
                object_name = record[i+2:len(record)]
                object_dict = object_list[len(object_list)-1]
                object_dict['OBJECT'] = object_name
                length_indicator = int.from_bytes(file.read(2), byteorder='little')
                #convert the record into a utf-8 char string
                record = file.read(length_indicator).decode('utf-8')
                if length_indicator % 2 != 0:
                    file.read(1)
                while(record[0:10]!="END_OBJECT"):
                    i = 1
                    while(record[i]!=' '):
                        i=i+1
                    name = record[1:i]
                    while(record[i]!='='):
                        i = i+1  
                    value = record[i+2:len(record)]
                    object_dict = object_list[len(object_list)-1]
                    object_dict[name] = value
                    length_indicator = int.from_bytes(file.read(2), byteorder='little')
                    #convert the record into a utf-8 char string
                    record = file.read(length_indicator).decode('utf-8')
                    if length_indicator % 2 != 0:
                        file.read(1)

            length_indicator = int.from_bytes(file.read(2), byteorder='little')
            
            #convert the record into a utf-8 char string
            record = file.read(length_indicator).decode('utf-8')

            if length_indicator % 2 != 0:
                file.read(1)

        #test
        '''
        print("******************* POINTER DICTIONARY *******************")
        print(pointer)
        print("")
        print("************** KEYWORD ASSIGMENT DICTIONARY **************")
        print(keyword_assignment)
        print()
        print("********************** OBJECT LIST ***********************")
        print(object_list)
        print()
        '''
        k=0
        image_histogram = []
        records_number = (int(pointer['^ENCODING_HISTOGRAM'])-int(pointer['^IMAGE_HISTOGRAM']))
        while(k<records_number):
            length_indicator = int.from_bytes(file.read(2), byteorder='little')
            for i in range(length_indicator//4):
                frequency = int.from_bytes(file.read(4), byteorder='little')
                image_histogram.append(frequency)
            if length_indicator % 2 != 0:
                file.read(1)
            k += 1
        '''
        print("********************** IMAGE_HISTOGRAM ***********************")
        print(image_histogram)
        print(sum(image_histogram))
        print(len(image_histogram))
        '''
        k=0
        encoding_histogram = []
        records_number = (int(pointer['^ENGINEERING_TABLE'])-int(pointer['^ENCODING_HISTOGRAM']))
        while(k<records_number):
            length_indicator = int.from_bytes(file.read(2), byteorder='little')
            for i in range(length_indicator//4):
                frequency = int.from_bytes(file.read(4), byteorder='little', signed=False)
                encoding_histogram.append(frequency)
            if length_indicator % 2 != 0:
                file.read(1)
            k += 1
        '''
        print("********************** ENCODING_HISTOGRAM ***********************")
        print(encoding_histogram)
        print(len(encoding_histogram))
        print(sum(encoding_histogram))
        '''


        class BinaryTree:

            def __init__(self, value = None, freq = None):
                self.value = value
                self.freq = freq
                self.left = None
                self.right = None
            
            def setValue(self, value):
                self.value = value

            def setFrequency(self, frequency):
                self.freq = int(frequency)

            def setLeft(self, tree):
                self.left = tree

            def setRight(self, tree):
                self.right = tree


            def getValue(self):
                return self.value

            def getFrequency(self):
                return self.freq

            def getLeft(self):
                return self.left

            def getRight(self):
                return self.right

            def isLeaf(self):
                if (self.left == None) and (self.right == None):
                    return True
                else:
                    return False

            def __repr__(self):
                return str(str(self.value)+" "+str(self.freq)+" ")

        def sortTree(tree_list):
            i = 1
            while(i<len(tree_list)):
                freq = tree_list[i].getFrequency()
                tree = tree_list[i]
                k = i-1
                while(k>=0 and freq<tree_list[k].getFrequency()):
                    tree_list[k+1] = tree_list[k]
                    k -= 1
                tree_list[k+1] = tree
                i += 1
            return tree_list

        tree_list = []

        i=0
        while(i<len(encoding_histogram)):
            if encoding_histogram[i] > 0:
                tree = BinaryTree(i+1, encoding_histogram[i])
                tree_list.append(tree)
            i+=1

        tree_list = sortTree(tree_list)

        while(len(tree_list) > 1):

            tree = BinaryTree()
            tree.setRight(tree_list.pop(0))
            tree.setLeft(tree_list.pop(0))
            tree.setFrequency(tree.getRight().getFrequency() + tree.getLeft().getFrequency())
            tree_list.insert(0, tree)

            i = 0
            while(i<len(tree_list)-1):
                if tree_list[i].getFrequency()>tree_list[i+1].getFrequency():
                    tmp = tree_list[i]
                    tree_list[i]=tree_list[i+1]
                    tree_list[i+1] = tmp
                else:
                    break
                i += 1

            #tree_list = sortTree(tree_list)
            

        import copy
        huffman_tree_root = tree_list.pop()
        node = copy.copy(huffman_tree_root)

        '''
        def explore(tree_root):
            if(tree_root.isLeaf()):
                print(tree_root.getValue())
            else:
                explore(tree_root.getLeft())
                explore(tree_root.getRight())

        explore(node)
        '''

        length_indicator = int.from_bytes(file.read(2), byteorder='little')
        engineering_table = file.read(length_indicator)
        if length_indicator % 2 != 0:
            file.read(1)

        #read compressed image
        def byteToBitList(line_byte):
            bit_list = []
            op = 128
            for i in range (8):
                if (line_byte & op) == op:
                    bit_list.append(1)
                else:
                    bit_list.append(0)
                op = op//2
            return bit_list

        image = []

        for k in range(800):

            length_indicator = int.from_bytes(file.read(2), byteorder='little', signed=False)
            first_sample = int.from_bytes(file.read(1), byteorder='little', signed=False)
            bit_list = []
            i = 1
            while(i<length_indicator):
                line_byte = int.from_bytes(file.read(1), byteorder='little', signed=False)
                bit_list = bit_list + byteToBitList(line_byte)
                i += 1

            if length_indicator % 2 != 0:
                file.read(1)

            image_line = []
            image_line.append(first_sample)


            for bit in bit_list:
                if bit == 1:
                    node = node.getLeft()
                
                else:
                    node = node.getRight()

                if node.isLeaf():
                    image_line.append(node.getValue())
                    node = copy.copy(huffman_tree_root)


            i=1
            while(i<800):
                image_line[i] =  -image_line[i]+image_line[i-1]+256
                i += 1

            image_line2 = []
            i=0
            while(i<800):
                a = tuple([image_line[i], 0, 0])
                image_line2.append(a)
                i += 1


            image.append(image_line2)

        '''
        check = []
        for k in range(256):
            count = 0
            for j in range(800):
                for i in range(800):
                    if(image[i][j][0]==k):
                        count += 1
            check.append(count)
        print(check)

        '''
        from PIL import Image
        import numpy as np
        # Convert the pixels into an array using numpy
        array = np.array(image, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array).convert('LA')


        import errno

        save = destination+fileName[len(source):len(fileName)-4]+'.png'

        if not os.path.exists(os.path.dirname(save)):
            try:
                os.makedirs(os.path.dirname(save))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        new_image.save(save)
        #close file
        file.close()
        file = open(save[:-4]+".info", "a")
        file.write(str(keyword_assignment)+"\n")
        for elem in object_list:
            file.write(str(elem)+"\n")
        file.write(str(pointer)+"\n")
        file.close()
    except IndexError:
        print("an error occured during the decompression of this image: corrupted or bad image")
        continue
    except UnicodeDecodeError:
        print("an error occured during the decompression of this image: invalid file format")
        continue
print("end")