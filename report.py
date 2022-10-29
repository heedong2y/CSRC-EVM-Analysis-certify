import os

#### EVM Bytecode Analysis performance certification
#### heedong@kaist.ac.kr

BENCHMARK_PATH = './benchmark/'
WORKDIR = './workdir/'

result = []
synonymous_opcode = {'keccak256':'sha3','pc':'getpc'}

def logging(msg, file):
    print(msg)
    file.write(msg+'\n')

def get_solc_opcode(path):
    opcodes = []
    f = open(path, "r")
    slices = f.readline().strip().split(' ')
    f.close()
    tmp = ''
    for item in slices:
        if len(item) == 0:
            continue
        elif item.startswith('PUSH'):
            tmp = item.lower()
        elif tmp != '':
            opcodes.append(tmp + ' ' + item.lower())
            tmp = ''
        else:
            opcodes.append(item.lower())
    return opcodes

def get_dissam_opcode(path):
    opcodes = []
    f = open(path, "r")
    dissam_list = f.readlines()
    f.close()
    for line in dissam_list:
        arr = line.replace(':',' ').split()
        if len(arr) == 0:
            continue
        elif len(arr) == 3:
            opcodes.append(arr[2].replace('(illegal)', (str('0x%x' % int(arr[1],16)))))
        else:
            opcodes.append(' '.join(arr[len(arr)-2 : ]))
    return opcodes

def evaluate(ans, target):
    for i, value in enumerate(ans):
        if value in synonymous_opcode:
            value = synonymous_opcode.get(value)
        if value == target[i]:
            continue
        else:
            print(" [diff] solc: %s disssamble: %s " % (value, target[i]))


def main():
    benchmark_file = os.listdir(BENCHMARK_PATH)
    benchmark_list = [file[:-4] for file in benchmark_file if file.endswith(".sol")]
    for sol in benchmark_list:
        test_res = dict()
        print("[*] " + sol + ".sol")
        dirname = WORKDIR + sol + '/'
        output_file = os.listdir(dirname)
        bin_list = [file[:-4] for file in output_file if file.endswith(".bin")]
        for binname in bin_list:
            print(binname)
            filesize = os.path.getsize(dirname + binname + '.bin')
            if filesize != 0:
                bin_op = get_solc_opcode(dirname + binname + '.opcode')
                bin_dis = get_dissam_opcode(dirname + binname + '.disam')
                evaluate(bin_op, bin_dis)



if __name__ == "__main__":
    main()
