
import sys
import numpy as np

class Node:
    def __init__(self):
        self.m_reff1    = -1.0
        self.m_reff2    = -1.0
        self.m_flag     = 0         # 0: x/x, 1: o/x, 2: x/o, 3: o/o
    def SetReff1(self, reff1):
        self.m_reff1    = reff1
    def GetReff1(self):
        return self.m_reff1
    def SetReff2(self, reff2):
        self.m_reff2    = reff2
    def GetReff2(self):
        return self.m_reff2
    def SetFlag(self, flag):
        self.m_flag = flag
    def GetFlag(self):
        return self.m_flag
    
class CompAllResXY:
    def __init__(self):
        self.m_output_prefix= ''
        self.m_filename1    = ''
        self.m_filename2    = ''
        self.m_node_dic     = {}    # key : x_y str, data : Node
    def Run(self, args):
        self.ReadArgs(args)
        self.PrintInputs()
        self.ReadFile1()
        self.ReadFile2()
        self.WriteOutputFiles()
    def PrintUsage(self):
        print(f'# usage comp_all_res_xy.py')
        print(f'python3 comp_all_res_xy.py output_prefix file1 file2')
    def ReadArgs(self, args):
        print(f'# read args start')
        if 4 != len(args):
            self.PrintUsage()
            exit()
        self.m_output_prefix    = args[1]
        self.m_filename1        = args[2]
        self.m_filename2        = args[3]
        print(f'# read args end')
    def PrintInputs(self):
        print(f'# print inputs start')
        print(f'    output prefix : {self.m_output_prefix}')
        print(f'    file1         : {self.m_filename1}')
        print(f'    file2         : {self.m_filename2}')
        print(f'# print inputs end')
    def ReadFile1(self):
        print(f'# read file1({self.m_filename1}) start')
        f = open(self.m_filename1, 'rt')
        while True:
            line = f.readline()
            if not line:
                break
            if 0 == len(line):
                continue
            tokens  = line.split()
            if 6 != len(tokens):
                continue
            key     = self.GetKey(tokens[2:4])
            reff    = float(tokens[4])
            if not key in self.m_node_dic:
                node    = Node()
                node.SetReff1(reff)
                node.SetFlag(1)
                self.m_node_dic[key]    = node
        f.close()
        print(f'# read file1({self.m_filename1}) end')
    def ReadFile2(self):
        print(f'# read file2({self.m_filename2}) start')
        f = open(self.m_filename2, 'rt')
        while True:
            line = f.readline()
            if not line:
                break
            if 0 == len(line):
                continue
            tokens  = line.split()
            if 6 != len(tokens):
                continue
            key     = self.GetKey(tokens[2:4])
            reff    = float(tokens[4])
            if key in self.m_node_dic:
                node    = self.m_node_dic[key]
                node.SetReff2(reff)
                node.SetFlag(3)
            else:
                node    = Node()
                node.SetReff2(reff)
                node.SetFlag(2)
                self.m_node_dic[key]    = node
        f.close()
        print(f'# read file2({self.m_filename2}) end')
    def WriteOutputFileBoth(self):
        filename    = self.m_output_prefix + '.both.txt'
        print(f'# write both output file({filename}) start')
        f = open(filename, 'wt')
        for key in self.m_node_dic:
            node = self.m_node_dic[key]
            if 3 == node.GetFlag():
                f.write(f'{key} {node.GetReff1()} {node.GetReff2()}\n')
        f.close()
        print(f'# write both output file({filename}) end')
    def WriteOutputFile1st(self):
        filename    = self.m_output_prefix + '.1st.txt'
        print(f'# write both output file({filename}) start')
        f = open(filename, 'wt')
        for key in self.m_node_dic:
            node = self.m_node_dic[key]
            if 1 == node.GetFlag():
                f.write(f'{key} {node.GetReff1()} {node.GetReff2()}\n')
        f.close()
        print(f'# write both output file({filename}) end')
    def WriteOutputFile2nd(self):
        filename    = self.m_output_prefix + '.2nd.txt'
        print(f'# write both output file({filename}) start')
        f = open(filename, 'wt')
        for key in self.m_node_dic:
            node = self.m_node_dic[key]
            if 2 == node.GetFlag():
                f.write(f'{key} {node.GetReff1()} {node.GetReff2()}\n')
        f.close()
        print(f'# write both output file({filename}) end')
    def WriteOutputFiles(self):
        self.WriteOutputFileBoth()
        self.WriteOutputFile1st()
        self.WriteOutputFile2nd()
    def GetKey(self, s):
        return '_'.join(s)

def main(args):
    my_comp_all_res_xy  = CompAllResXY()
    my_comp_all_res_xy.Run(args)

if __name__ == '__main__':
    main(sys.argv)