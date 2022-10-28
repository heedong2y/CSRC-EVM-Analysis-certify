import os
import sys
import time

#### EVM Bytecode Analysis performance certification
#### heedong@kaist.ac.kr

TEST_MODULE_PATH = './B2R2/src/RearEnd/BinDump/bin/Release/net6.0/B2R2.RearEnd.BinDump'
BENCHMARK_PATH = './benchmark/'
WORKDIR = './workdir/'
SOLC_PATH  = './solc-0.4.25'  # Solidity compiler
OUTPUT_DIR = './output'

opcode_ref = dict()
test_bytecodes = []
disasm_opcodes = []
lifting_opcodes = []


# EVM bytecode disassemble
def read_bin(dir, binfile):
    f = open(dir + '/' +binfile, "r")
    bytecode = f.read()
    f.close()
    print (len(bytecode))
    return bytecode

def disassemble_evm(dir, binfile, bytecode):
    disasm_output = []
    if len(bytecode) % 2 != 0:
        print(binfile + " is wrong bytecode")
    elif len(bytecode) == 0:
        print(binfile + " is emtpy")
    else:
        disasm_cmd = (' -i evm -s %s' % bytecode)
        disasm_res = os.popen(TEST_MODULE_PATH + disasm_cmd)
        disasm_output = disasm_res.readlines()
    f = open(dir + '/' + binfile[:-4] + ".disam", "w")
    f.writelines(disasm_output)
    f.close()

def main():
    benchmark_file = os.listdir(BENCHMARK_PATH)
    benchmark_list = [file[:-4] for file in benchmark_file if file.endswith(".sol")]
    for sol in benchmark_list:
        dirname = WORKDIR + sol
        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        except OSError:
            print ('Creating directory Error:' + dirname)
        os.system(SOLC_PATH + ' -o %s --opcodes --bin %s' % (dirname, BENCHMARK_PATH + sol + '.sol'))
        output_file = os.listdir(dirname)
        bin_list = [file for file in output_file if file.endswith(".bin")]
        for bin in bin_list:
            bytecode = read_bin(dirname, bin)
            disassemble_evm(dirname, bin, bytecode)
        pirnt(bin[:-4] + " disassemble & lifting done.")

    logging("[*] Experiment compleated %ds" % (time.time() - start), diff_log)

if __name__ == "__main__":
    main()


