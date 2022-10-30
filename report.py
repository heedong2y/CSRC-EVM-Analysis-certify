import os

#### EVM Bytecode Analysis performance certification
#### heedong@kaist.ac.kr

BENCHMARK_PATH = './benchmark/'
WORKDIR = './workdir/'

result = dict()
synonymous_opcode = {'keccak256':'sha3','pc':'getpc'}

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

def evaluate(binname, ans, target, logfile):
    matchCnt = 0
    for i, value in enumerate(ans):
        if value in synonymous_opcode:
            value = synonymous_opcode.get(value)
        if value == target[i]:
            matchCnt += 1
        else:
            logfile.write(" [Diff] %s.bin / solc: %s / disssamble: %s\n" % (binname, value, target[i]))
    return matchCnt

def report():
    evalTotal = 0
    evalMatch = 0
    print("\n\n[*] Report")
    for key in result:
        evalMatch += result[key][0]
        evalTotal += result[key][1]
        try: 
            print("%s : %d / %d (%.1f%%)" % (key, result[key][0], result[key][1], (float(result[key][0]) / float(result[key][1]) * 100.0)))
        except ZeroDivisionError:
            print("0 / 0 (100.0%)")
    try: 
        print("\n[*] Total Result : %d / %d (%.1f%%)" % (evalMatch, evalTotal, (float(evalMatch) / float(evalTotal) * 100.0)))
    except ZeroDivisionError:
        print("\n[*] Total Result : 0 / 0 (100.0%)")


def main():
    benchmark_file = os.listdir(BENCHMARK_PATH)
    benchmark_list = [file[:-4] for file in benchmark_file if file.endswith(".sol")]
    
    for sol in benchmark_list:
        print("[*] " + sol + ".sol")
        dirname = WORKDIR + sol + '/'
        difflog = open(dirname + '/' + sol + "_diff.log", "w")
        output_file = os.listdir(dirname)
        bin_list = [file[:-4] for file in output_file if file.endswith(".bin")]
        totalCnt = 0
        matchCnt = 0
        for binname in bin_list:
            bin_totalCnt = 0
            bin_matchCnt = 0
            filesize = os.path.getsize(dirname + binname + '.bin')
            if filesize != 0:
                bin_op = get_solc_opcode(dirname + binname + '.opcode')
                bin_dis = get_dissam_opcode(dirname + binname + '.disam')
                bin_totalCnt = len(bin_op)
                bin_matchCnt = evaluate(binname, bin_op, bin_dis, difflog)
                totalCnt += bin_totalCnt 
                matchCnt += bin_matchCnt
            print(" %s.bin : %d / %d" % (binname, bin_matchCnt, bin_totalCnt))
        result[sol] = [matchCnt, totalCnt]
        difflog.close()
    
    report()

if __name__ == "__main__":
    main()
