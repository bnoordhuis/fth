import re
import sys


def isblank(c):
    return c in '\t\r\n '


def lex(s, i, n):
    while i < n and isblank(s[i]):
        i += 1

    j = i + 1

    while j < n and not isblank(s[j]):
        j += 1

    return i, j


def parse(s, i, n):
    while i < n:
        i, j = lex(s, i, n)

        if s[i:j] == '(':
            while j < n:
                i, j = lex(s, j, n)

                if s[i:j] == ')':
                    break
        elif s[i:j] == '\\':
            while j < n and s[j] != '\n':
                j += 1
        else:
            return i, j

        i = j

    return n, n # eof


def compile(s):
    print('''
attributes #0 = { norecurse nounwind alwaysinline }
declare i32 @fputc(i32, i8* nocapture) nounwind
@stdout = external global i8*
@A = private unnamed_addr global i64 0
@B = private unnamed_addr global i64 0
@C = private unnamed_addr global i64 0
@SP = private unnamed_addr global i64* null
define hidden i32 @main(i32 %argc, i8** %argv) norecurse nounwind {
  %ds = alloca [1024 x i64]
  %sp = getelementptr [1024 x i64], [1024 x i64]* %ds, i64 0, i64 0
  store i64* %sp, i64** @SP
  call fastcc void @_main()
  ret i32 0
}
define hidden fastcc void @a() #0 section ".text.a" {
  %1 = ptrtoint i64* @A to i64
  call fastcc void @push(i64 %1)
  ret void
}
define hidden fastcc void @b() #0 section ".text.b" {
  %1 = ptrtoint i64* @B to i64
  call fastcc void @push(i64 %1)
  ret void
}
define hidden fastcc void @c() #0 section ".text.c" {
  %1 = ptrtoint i64* @C to i64
  call fastcc void @push(i64 %1)
  ret void
}
define hidden fastcc void @and() #0 section ".text.and" {
  %1 = call fastcc i64 @pop()
  %2 = call fastcc i64 @pop()
  %3 = and i64 %2, %1
  call fastcc void @push(i64 %3)
  ret void
}
define hidden fastcc void @div() #0 section ".text.div" {
  %1 = call fastcc i64 @pop()
  %2 = call fastcc i64 @pop()
  %3 = urem i64 %2, %1
  %4 = udiv i64 %2, %1
  call fastcc void @push(i64 %3)
  call fastcc void @push(i64 %4)
  ret void
}
;define hidden fastcc void @drop() #0 section ".text.drop" {
;  call fastcc i64 @pop()
;  ret void
;}
;define hidden fastcc void @dup() #0 section ".text.dup" {
;  %1 = call fastcc i64 @pop()
;  call fastcc void @push(i64 %1)
;  call fastcc void @push(i64 %1)
;  ret void
;}
define hidden fastcc void @emit() #0 section ".text.emit" {
  %1 = call fastcc i64 @pop()
  %2 = trunc i64 %1 to i32
  %stdout = load i8*, i8** @stdout
  call i32 @fputc(i32 %2, i8* %stdout)
  ret void
}
define hidden fastcc void @load() #0 section ".text.load" {
  %1 = call fastcc i64 @pop()
  %2 = inttoptr i64 %1 to i64*
  %3 = load i64, i64* %2
  call fastcc void @push(i64 %3)
  ret void
}
define hidden fastcc void @lt() #0 section ".text.lt" {
  %1 = call fastcc i64 @pop()
  %2 = call fastcc i64 @pop()
  %3 = icmp slt i64 %2, %1
  %4 = sext i1 %3 to i64
  call fastcc void @push(i64 %4)
  ret void
}
define hidden fastcc i64 @pop() #0 section ".text.pop" {
  %1 = load i64*, i64** @SP
  %2 = getelementptr i64, i64* %1, i64 -1
  %3 = load i64, i64* %2
  store i64* %2, i64** @SP
  ret i64 %3
}
define hidden fastcc void @push(i64) #0 section ".text.push" {
  %2 = load i64*, i64** @SP
  %3 = getelementptr i64, i64* %2, i64 1
  store i64 %0, i64* %2
  store i64* %3, i64** @SP
  ret void
}
define hidden fastcc void @store() #0 section ".text.store" {
  %1 = call fastcc i64 @pop()
  %2 = call fastcc i64 @pop()
  %3 = inttoptr i64 %1 to i64*
  store i64 %2, i64* %3
  ret void
}
define hidden fastcc void @sub() #0 section ".text.sub" {
  %1 = call fastcc i64 @pop()
  %2 = call fastcc i64 @pop()
  %3 = sub i64 %2, %1
  call fastcc void @push(i64 %3)
  ret void
}
;define hidden fastcc void @swap() #0 section ".text.swap" {
;  %1 = call fastcc i64 @pop()
;  %2 = call fastcc i64 @pop()
;  call fastcc void @push(i64 %1)
;  call fastcc void @push(i64 %2)
;  ret void
;}
define hidden fastcc void @xor() #0 section ".text.xor" {
  %1 = call fastcc i64 @pop()
  %2 = call fastcc i64 @pop()
  %3 = xor i64 %1, %2
  call fastcc void @push(i64 %3)
  ret void
}
''')

    M = {
        '!'   : 'store',
        '-'   : 'sub',
        '<'   : 'lt',
        '@'   : 'load',
        'a'   : 'a',
        'and' : 'and',
        'b'   : 'b',
        'c'   : 'c',
        'div' : 'div',
        'drop': 'drop',
        'dup' : 'dup',
        'emit': 'emit',
        'main': '_main',
        'swap': 'swap',
        'xor' : 'xor',
    }

    def mangle(w):
        return M.setdefault(w, 'g' + str(len(M)))

    def varsym():
        varsym.n += 1
        return str(varsym.n)
    varsym.n = 0

    def labelsym():
        labelsym.n += 1
        return 'L' + str(labelsym.n)
    labelsym.n = 0

    i = 0
    n = len(s)
    r = []
    branches = []

    while i < n:
        i, j = parse(s, i, n)

        w = s[i:j]
        i = j

        if w == '':
            break # eof

        if w == ':':
            i, j = parse(s, i, n)

            w = mangle(s[i:j])
            i = j

            print('define hidden fastcc void @' + w +
                  '() #0 section ".text.' + w + '" {')
            labelsym.n = 0
            varsym.n = 0
            continue

        if w == ';':
            print('  ret void')
            print('}')
            continue

        if w == 'if':
            q = varsym()
            r = varsym()
            yes = labelsym()
            no = labelsym()
            end = labelsym()
            print('  %' + q + ' = call fastcc i64 @pop()')
            print('  %' + r + ' = icmp ne i64 %' + q + ', 0')
            print('  br i1 %' + r + ', label %' + yes + ', label %' + no)
            print(yes + ':')
            branches.append((no, end))
            continue

        if w == 'else':
            no, end = branches.pop()
            branches.append((None, end))
            print('  br label %' + end)
            print(no + ':')
            continue

        if w == 'then':
            no, end = branches.pop()
            print('  br label %' + end)
            if no:
                print(no + ':')
                print('  br label %' + end)
            print(end + ':')
            continue

        try:
            x = int(w)
        except ValueError:
            x = None

        if x is None:
            if w not in M:
                raise Exception('undefined word: ' + w)
            print('  call fastcc void @' + mangle(w) + '()')
        else:
            print('  call fastcc void @push(i64 ' + w + ')')


def main(argv):
    s = sys.stdin.read()
    compile(s)


if __name__ == '__main__':
    main(sys.argv[:])
