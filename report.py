import os

#### EVM Bytecode Analysis performance certification
#### heedong@kaist.ac.kr

BENCHMARK_PATH = './benchmark/benchmark1/'
WORKDIR = './workdir/'

result = dict()
synonymous_opcode = {'keccak256':'sha3','pc':'getpc'}

def get_opcode(path):
    opcodes = []
    f = open(path, "r")
    slices = f.readline().strip().split(' ')
    f.close()
    tmp = ''
    for item in slices:
        if len(item) == 0:
            continue
        elif item.lower().startswith('push'):
            tmp = item.lower()
        elif tmp != '':
            opcodes.append(tmp + ' ' + item.lower())
            tmp = ''
        else:
            opcodes.append(item.lower())
    return opcodes

def evaluate(binname, ans, target, logfile):
    matchCnt = 0
    for i, value in enumerate(ans):
        if value in synonymous_opcode:
            value = synonymous_opcode.get(value)
        if value == target[i]:
            matchCnt += 1
        else:
            diff_msg = " [Diff] %s.bin / solc: %s / disssamble: %s\n" % (binname, value, target[i])
            logfile.write(diff_msg)
            print(diff_msg)
    return matchCnt

def report():
    evalTotal = 0
    evalMatch = 0
    print("\n\n[*] Report")
    for key in result:
        evalMatch += result[key][0]
        evalTotal += result[key][1]
        try:
            print(" %s.sol : %d / %d (%.2f%%)" % (key, result[key][0], result[key][1], (float(result[key][0]) / float(result[key][1]) * 100.0)))
        except ZeroDivisionError:
            print("0 / 0 (100.0%)")
    try:
        print("\n[*] Total Result : %d / %d (%.2f%%)" % (evalMatch, evalTotal, (float(evalMatch) / float(evalTotal) * 100.0)))
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
                bin_op = get_opcode(dirname + binname + '.opcode')
                bin_dis = get_opcode(dirname + binname + '.disam')
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
