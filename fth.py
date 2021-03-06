import re
import sys


def compile(s):
    print('''
attributes #0 = { norecurse nounwind alwaysinline }
declare i32 @fputc(i32, i8* nocapture) nounwind
@stdout = external global i8*
@A = private unnamed_addr global i64 0
@B = private unnamed_addr global i64 0
@C = private unnamed_addr global i64 0
define hidden i32 @main(i32 %argc, i8** %argv) norecurse nounwind {
  %ds = alloca [1024 x i64]
  %sp = getelementptr [1024 x i64], [1024 x i64]* %ds, i64 0, i64 0
  %spp = alloca i64*
  store i64* %sp, i64** %spp
  call fastcc void @_main(i64** %spp)
  ret i32 0
}
define hidden fastcc void @a(i64** %spp) #0 section ".text.a" {
  %1 = ptrtoint i64* @A to i64
  call fastcc void @push(i64** %spp, i64 %1)
  ret void
}
define hidden fastcc void @b(i64** %spp) #0 section ".text.b" {
  %1 = ptrtoint i64* @B to i64
  call fastcc void @push(i64** %spp, i64 %1)
  ret void
}
define hidden fastcc void @c(i64** %spp) #0 section ".text.c" {
  %1 = ptrtoint i64* @C to i64
  call fastcc void @push(i64** %spp, i64 %1)
  ret void
}
define hidden fastcc void @and(i64** %spp) #0 section ".text.and" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = call fastcc i64 @pop(i64** %spp)
  %3 = and i64 %2, %1
  call fastcc void @push(i64** %spp, i64 %3)
  ret void
}
define hidden fastcc void @div(i64** %spp) #0 section ".text.div" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = call fastcc i64 @pop(i64** %spp)
  %3 = urem i64 %2, %1
  %4 = udiv i64 %2, %1
  call fastcc void @push(i64** %spp, i64 %3)
  call fastcc void @push(i64** %spp, i64 %4)
  ret void
}
define hidden fastcc void @emit(i64** %spp) #0 section ".text.emit" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = trunc i64 %1 to i32
  %stdout = load i8*, i8** @stdout
  call i32 @fputc(i32 %2, i8* %stdout)
  ret void
}
define hidden fastcc void @load(i64** %spp) #0 section ".text.load" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = inttoptr i64 %1 to i64*
  %3 = load i64, i64* %2
  call fastcc void @push(i64** %spp, i64 %3)
  ret void
}
define hidden fastcc i64 @pop(i64** %spp) #0 section ".text.pop" {
  %1 = load i64*, i64** %spp
  %2 = getelementptr i64, i64* %1, i64 -1
  %3 = load i64, i64* %2
  store i64* %2, i64** %spp
  ret i64 %3
}
define hidden fastcc void @push(i64** %spp, i64) #0 section ".text.push" {
  %2 = load i64*, i64** %spp
  %3 = getelementptr i64, i64* %2, i64 1
  store i64 %0, i64* %2
  store i64* %3, i64** %spp
  ret void
}
define hidden fastcc void @store(i64** %spp) #0 section ".text.store" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = call fastcc i64 @pop(i64** %spp)
  %3 = inttoptr i64 %1 to i64*
  store i64 %2, i64* %3
  ret void
}
define hidden fastcc void @sub(i64** %spp) #0 section ".text.sub" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = call fastcc i64 @pop(i64** %spp)
  %3 = sub i64 %2, %1
  call fastcc void @push(i64** %spp, i64 %3)
  ret void
}
define hidden fastcc void @xor(i64** %spp) #0 section ".text.xor" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = call fastcc i64 @pop(i64** %spp)
  %3 = xor i64 %1, %2
  call fastcc void @push(i64** %spp, i64 %3)
  ret void
}
define hidden fastcc void @zeq(i64** %spp) #0 section ".text.zeq" {
  %1 = call fastcc i64 @pop(i64** %spp)
  %2 = icmp eq i64 %1, 0
  %3 = sext i1 %2 to i64
  call fastcc void @push(i64** %spp, i64 %3)
  ret void
}
''')

    M = {
        '!'   : 'store',
        '-'   : 'sub',
        '0='  : 'zeq',
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

    s = re.sub(r'\\.*\n', '', s) # strip line comments
    t = s.split()
    branches = []

    while t:
        w = t.pop(0)

        if w == '':
            break # eof

        if w == '(':
            while ')' != t.pop(0):
                pass
            continue

        if w == ':':
            w = mangle(t.pop(0))
            print('define hidden fastcc void @' + w +
                  '(i64** %spp) #0 section ".text.' + w + '" {')
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
            print('  %' + q + ' = call fastcc i64 @pop(i64** %spp)')
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
            x = int(w[1:], 16) if w.startswith('$') else int(w)
        except ValueError:
            x = None

        if x is None:
            if w not in M:
                raise Exception('undefined word: ' + w)
            print('  call fastcc void @' + mangle(w) + '(i64** %spp)')
        else:
            print('  call fastcc void @push(i64** %spp, i64 ' + str(x) + ')')


def main(argv):
    s = sys.stdin.read()
    compile(s)


if __name__ == '__main__':
    main(sys.argv[:])
