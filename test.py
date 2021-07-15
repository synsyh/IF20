"""
IF20-test by Yuning Sun
7:48 PM 5/17/21
Module documentation: 
"""


def main():
    pass


if __name__ == '__main__':
    vs = [(1, 2), (2, 3), (3, 4)]
    hs = [(1, 2), (3, 4), (4, 6)]
    cmds = ['sdfad', 'dsafasdf', 'ewrwer']
    with open('test.txt', 'w') as f:
        for i in range(len(vs)):
            f.write(str(vs[i]) + '\t' + str(hs[i]) + '\t' + cmds[i] + '\r\n')
