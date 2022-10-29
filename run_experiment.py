import os
import sys
import time
import subprocess

#### EVM Bytecode Analysis performance certification
#### heedong@kaist.ac.kr

SOLC_PATH  = './solc-0.8.17'  # Solidity compiler
TEST_MODULE_PATH = './B2R2/src/RearEnd/BinDump/bin/Release/net6.0/B2R2.RearEnd.BinDump'
BENCHMARK_PATH = './benchmark/'
WORKDIR = './workdir/'
OUTPUT_DIR = './output'


def solc_compile(dirname, sol):
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    except OSError:
        print ('Creating directory Error:' + dirname)
        sys.exit(1)
    f = open(dirname + '/' + "sol_compile.log", "w")
    s_compile = subprocess.Popen([SOLC_PATH ,'-o', dirname,'--opcodes', '--bin', BENCHMARK_PATH + sol + '.sol'], stderr=subprocess.PIPE)
    error = s_compile.stderr.readlines()
    for msg in error:
        f.write(msg.decode('utf-8')+'\n')
    f.close()

def read_bin(dir, binfile):
    f = open(dir + '/' +binfile, "r")
    bytecode = f.read()
    f.close()
    return bytecode

def disassemble_evm(dir, binfile, bytecode):
    disasm_output = []
    if len(bytecode) % 2 != 0:
        print("  [Disassamble] " + binfile + " is wrong bytecode")
    elif len(bytecode) == 0:
        print("  [Disassamble] "+ binfile + " is emtpy")
    else:
        disasm_cmd = (' -i evm -s %s' % bytecode)
        disasm_res = os.popen(TEST_MODULE_PATH + disasm_cmd)
        disasm_output = disasm_res.readlines()
        print("  [Disassamble] " + binfile + " disassam done.")
    f = open(dir + '/' + binfile[:-4] + ".disam", "w")
    f.writelines(disasm_output)
    f.close()

def lifting_evm(dir, binfile, bytecode):
    lift_output = []
    if len(bytecode) % 2 != 0:
        print("  [Lifting] " + binfile + " is wrong bytecode")
    elif len(bytecode) == 0:
        print("  [Lifting] " + binfile + " is emtpy")
    else:
        lift_cmd = (' -i evm -s %s --lift' % bytecode)
        lift_res = os.popen(TEST_MODULE_PATH + lift_cmd)
        lift_output = lift_res.readlines()
        print("  [Lifting] " + binfile + " lifting done.")
    f = open(dir + '/' + binfile[:-4] + ".lift", "w")
    f.writelines(lift_output)
    f.close()

def main():
    benchmark_file = os.listdir(BENCHMARK_PATH)
    benchmark_list = [file[:-4] for file in benchmark_file if file.endswith(".sol")]
    start = time.time()
    for sol in benchmark_list:
        print("[*] " + sol + ".sol experiment started")
        dirname = WORKDIR + sol
        solc_compile(dirname, sol)
        output_file = os.listdir(dirname)
        bin_list = [file for file in output_file if file.endswith(".bin")]
        for bin in bin_list:
            bytecode = read_bin(dirname, bin)
            disassemble_evm(dirname, bin, bytecode)
            lifting_evm(dirname, bin, bytecode)

    print("[*] Experiment compleated %ds" % (time.time() - start))

if __name__ == "__main__":
    main()


