import pickle
from datetime import time
from functools import reduce, partial
import random
import matplotlib as matplotlib
from tkinter import *
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from matplotlib.figure import Figure
import time
import matplotlib.pyplot as plt


def RefreshGraf1():
    global keybit, intervals

    for i in range(len(keybit)):
        minimum = i
        for j in range(i + 1, len(keybit)):
            # Выбор наименьшего значения
            if keybit[j] < keybit[minimum]:
                minimum = j
        # Помещаем это перед отсортированным концом массива
        keybit[minimum], keybit[i] = keybit[i], keybit[minimum]
        intervals[minimum], intervals[i] = intervals[i], intervals[minimum]
    intervals.reverse()
    keybit.reverse()

    plt.grid()  # включение отображение сетки
    plt.title("Зависимость времени факторизации от длины ключа")
    plt.xlabel("Время, с")
    plt.ylabel("Длина ключа, бит")
    plt.plot(keybit, intervals)
    plt.show()


def RefreshGraf2():
    r = []
    interval = []
    for i in range(25,50,5):
        i = i/100
        r.append(i)
        l2.config(text='')
        if (key_len.get().isdigit()):
            L = int(key_len.get())
        else:
            L = 128
            if (key_len.get() != ''):
                l2.config(text="(Некорректный формат введенных данных)")

        p = numberGenerate(int(L*i))
        print(int(L*i), int(L*(1-i)))
        q = numberGenerate(int(L*(1-i)))
        n = p * q
        eiler = (p - 1) * (q - 1)

        e = 257
        i = 0
        while (efclide(eiler, e) != 1):
            e = numFerma(i)
            i += 1

        d = efclideEx(e, eiler)
        if (d < 0):
            d += eiler

        PublicKey = [e, n]
        PrivateKey = [d, n]

        x, y, i, stage = random.randint(1, n - 1), 1, 0, 2
        start = time.time()
        while (efclide(n, abs(x - y)) == 1):
            if (i == stage):
                y = x
                stage = stage * 2
            x = (x * x + 1) % n
            i = i + 1

        p = efclide(n, abs(x - y))
        q = int(n / p)
        eiler = (p - 1) * (q - 1)

        d = efclideEx(e, eiler)
        if (d < 0):
            d += eiler

        end = time.time()
        interval.append((end - start))

        print(interval)
        print(r)
        print("\nПодобранный ключ:")
        print(d)

    plt.grid()  # включение отображение сетки
    plt.title("Зависимость времени факторизации от r")
    plt.xlabel("Величина r")
    plt.ylabel("Время, с")
    plt.plot(r, interval)
    plt.show()


def chooseFile():
    file_name = fd.askopenfilename()
    return file_name


def crypt():
    file_name = chooseFile()
    tmp, file_extension = os.path.splitext(file_name)

    if (key_len.get().isdigit()):
        L = int(key_len.get())
    else:
        L = 128

    step = L // 4

    OpenMessage = ''
    with open(file_name, 'rb') as file:
        fb = file.read()
        for i in fb:
            OpenMessage += ''.join("{:08b}".format(i, 'b'))
    print(OpenMessage)

    if(file_extension == ".jpg"):
        M = []
        preambula = []
        preambula_len = 700
        for i in range(0, preambula_len * 8, 8):
            preambula.append(OpenMessage[i:i+8])
        for i in range(preambula_len * 8, len(OpenMessage), step):
            M.append(OpenMessage[i:i + step])
        print(M)
        print(len(M))
        print(len(OpenMessage) - preambula_len*8)
        print((len(OpenMessage) - preambula_len*8) // step - 1)
        last_item_len = len(M[(len(OpenMessage) - preambula_len*8) // step - 1])
    else:
        if (file_extension == ".mp3"):
            M = []
            preambula = []
            preambula_len = 64000
            for i in range(0, preambula_len * 8, 8):
                preambula.append(OpenMessage[i:i + 8])
            for i in range(preambula_len * 8, len(OpenMessage), step):
                M.append(OpenMessage[i:i + step])
            print(M)
            print(len(M))
            print(len(OpenMessage) - preambula_len * 8)
            print((len(OpenMessage) - preambula_len * 8) // step - 1)
            last_item_len = len(M[(len(OpenMessage) - preambula_len * 8) // step - 1])
        else:
            M = []
            for i in range(0, len(OpenMessage), step):
                M.append(OpenMessage[i:i + step])
            last_item_len = len(M[len(OpenMessage) // step])

    if (var.get() == False):  # Сгенерировать ключи
        e, n, d = keyGenerate()
    if (var.get()): # Загрузить ключи из файла
        with open("C:/Users/Airat/Desktop/lab3_PublicKey.txt", 'r', encoding='utf-8') as file:
            Key = ['','']
            index = 0
            tmp = []
            for i in file.read():
                if (i == ' '):
                    Key[index] = ''.join(str(tmp[j]) for j in range(len(tmp)))
                    index = 1
                    tmp = []
                else:
                    tmp.append(i)
                Key[index] = ''.join(str(tmp[j]) for j in range(len(tmp)))
            file.close()
        e = int(Key[0])
        n = int(Key[1])

    C = []
    for i in range(0,len(M)):
        C.append(fastPowNod(int(M[i],2),e,n))

    if(file_extension == ".jpg"):
        with open("C:/Users/Airat/Desktop/lab3_cryptImage"+file_extension, 'wb') as file:
            for i in range(len(preambula)):
                file.write(int(preambula[i],2).to_bytes(1, "big"))
            for i in range(0, len(C)):
                file.write(C[i].to_bytes(L, "big"))
            file.write(L.to_bytes(2, "big"))
            file.write(last_item_len.to_bytes(2, "big"))
        file.close()
    else:
        if (file_extension == ".mp3"):
            with open("C:/Users/Airat/Desktop/lab3_cryptSound" + file_extension, 'wb') as file:
                for i in range(len(preambula)):
                    file.write(int(preambula[i], 2).to_bytes(1, "big"))
                for i in range(0, len(C)):
                    file.write(C[i].to_bytes(L, "big"))
                file.write(L.to_bytes(2, "big"))
                file.write(last_item_len.to_bytes(2, "big"))
            file.close()
        else:
            with open("C:/Users/Airat/Desktop/lab3_crypt.txt", 'wb') as file:
                for i in range(0, len(C)):
                    file.write(C[i].to_bytes(L, "big"))
                file.write(L.to_bytes(2, "big"))
                file.write(last_item_len.to_bytes(2, "big"))
            file.close()

    try:
        with open("C:/Users/Airat/Desktop/lab3_crypt.txt", 'r', encoding='ANSI') as file:
            df = file.read()
            file.close()
    except:
        df = "Ошибка при чтении файла!"

    if (file_extension == ".jpg"):
        try:
            with open("C:/Users/Airat/Desktop/lab3_CryptImage" + file_extension, 'r', encoding='ANSI') as file:
                f = file.read()
        except: f = "Ошибка при чтении файла!"
    else:
        if (file_extension == ".mp3"):
            try:
                with open("C:/Users/Airat/Desktop/lab3_CryptSound" + file_extension, 'r', encoding='ANSI') as file:
                    f = file.read()
            except:
                f = "Ошибка при чтении файла!"
        else:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    f = file.read()
            except:
                try:
                    with open(file_name, 'r', encoding='ANSI') as file:
                        f = file.read()
                except:
                    f = "Ошибка при чтении файла!"


    text1.delete(1.0, END)
    text2.delete(1.0, END)
    text1.insert(1.0, "Открытый текст:\n" + f)
    text2.insert(1.0, "Зашифрованный текст:\n" + df)


def deCrypt():
    file_name = chooseFile()
    tmp, file_extension = os.path.splitext(file_name)

    if (key_len.get().isdigit()):
        L = int(key_len.get())
    else:
        L = 128

    step = L // 4

    if (var.get() == False): # Сгенерировать ключи
        e, n, d = keyGenerate()
    if (var.get()): # Загрузить ключи из файла
        with open("C:/Users/Airat/Desktop/lab3_PrivateKey.txt", 'r', encoding='utf-8') as file:
            Key = ['','']
            index = 0
            tmp = []
            for i in file.read():
                if (i == ' '):
                    Key[index] = ''.join(str(tmp[j]) for j in range(len(tmp)))
                    index = 1
                    tmp = []
                else:
                     tmp.append(i)
            Key[index] = ''.join(str(tmp[j]) for j in range(len(tmp)))
        file.close()
        d = int(Key[0])
        n = int(Key[1])

    if (file_extension == ".jpg"):
        M = []
        preambula = []
        preambula_len = 700
        with open(file_name, 'rb') as file:
            fb = file.read()
            preambula = fb[:preambula_len]
            print(preambula)
            if (var.get()):
                L = int.from_bytes(fb[len(fb) - 4:len(fb) - 2], "big")
            last_item_len = int.from_bytes(fb[len(fb) - 2:], "big")
            print(last_item_len)
            for i in range(preambula_len, len(fb) - 4 - L, L):
                M.append("{0:0{1}b}".format(fastPowNod(int.from_bytes(fb[i:i + L], "big"), d, n), L // 4))
            M.append("{0:0{1}b}".format(fastPowNod(int.from_bytes(fb[len(fb) - 4 - L:len(fb) - 4], "big"), d, n),
                                        last_item_len))
    else:
        if (file_extension == ".mp3"):
            M = []
            preambula = []
            preambula_len = 64000
            with open(file_name, 'rb') as file:
                fb = file.read()
                preambula = fb[:preambula_len]
                print(preambula)
                if (var.get()):
                    L = int.from_bytes(fb[len(fb) - 4:len(fb) - 2], "big")
                last_item_len = int.from_bytes(fb[len(fb) - 2:], "big")
                print(last_item_len)
                for i in range(preambula_len, len(fb) - 4 - L, L):
                    M.append("{0:0{1}b}".format(fastPowNod(int.from_bytes(fb[i:i + L], "big"), d, n), L // 4))
                M.append("{0:0{1}b}".format(fastPowNod(int.from_bytes(fb[len(fb) - 4 - L:len(fb) - 4], "big"), d, n),
                                            last_item_len))
        else:
            M = []
            with open(file_name, 'rb') as file:
                fb = file.read()
                if (var.get()):
                    L = int.from_bytes(fb[len(fb) - 4:len(fb) - 2], "big")
                last_item_len = int.from_bytes(fb[len(fb) - 2:], "big")
                for i in range(0, len(fb) - 4 - L, L):
                    M.append("{0:0{1}b}".format(fastPowNod(int.from_bytes(fb[i:i + L], "big"), d, n), L // 4))
                M.append("{0:0{1}b}".format(fastPowNod(int.from_bytes(fb[len(fb) - 4 - L:len(fb) - 4], "big"), d, n),
                                            last_item_len))

    DeCryptMessage = ''.join(M)

    if (file_extension == ".jpg"):
        with open("C:/Users/Airat/Desktop/lab3_deCryptImage"+file_extension, 'wb') as file:
            file.write(preambula)
            for i in range(0, len(DeCryptMessage), 8):
                file.write(int(DeCryptMessage[i:i + 8], 2).to_bytes(1, "big"))
            file.close()
    else:
        if (file_extension == ".mp3"):
            with open("C:/Users/Airat/Desktop/lab3_deCryptSound" + file_extension, 'wb') as file:
                file.write(preambula)
                for i in range(0, len(DeCryptMessage), 8):
                    file.write(int(DeCryptMessage[i:i + 8], 2).to_bytes(1, "big"))
                file.close()
        else:
            with open("C:/Users/Airat/Desktop/lab3_deCrypt.txt", 'wb') as file:
                for i in range(0, len(DeCryptMessage), 8):
                    file.write(int(DeCryptMessage[i:i + 8], 2).to_bytes(1, "big"))
                file.close()

    try:
        with open(file_name, 'r', encoding='ANSI') as file:
            df = file.read()
            file.close()
    except:
        df = "Ошибка при чтении файла!"

    if (file_extension == ".jpg"):
        try:
            with open("C:/Users/Airat/Desktop/lab3_deCryptImage" + file_extension, 'r', encoding='ANSI') as file:
                f = file.read()
        except: f = "Ошибка при чтении файла!"
    else:
        if (file_extension == ".mp3"):
            try:
                with open("C:/Users/Airat/Desktop/lab3_deCryptSound" + file_extension, 'r', encoding='ANSI') as file:
                    f = file.read()
            except:
                f = "Ошибка при чтении файла!"
        else:
            try:
                with open("C:/Users/Airat/Desktop/lab3_deCrypt.txt", 'r', encoding='utf-8') as file:
                    f = file.read()
            except:
                try:
                    with open("C:/Users/Airat/Desktop/lab3_deCrypt.txt", 'r', encoding='ANSI') as file:
                        f = file.read()
                except:
                    f = "Ошибка при чтении файла!"

    text1.delete(1.0, END)
    text2.delete(1.0, END)
    text1.insert(1.0, "Зашифрованный текст:\n" + df)
    text2.insert(1.0, "Расшифрованный текст:\n" + f)


def polardAttack():
    global intervals, keybit

    if (var.get() == False): # Сгенерировать ключи
        e, n, d = keyGenerate()
    if (var.get()): # Загрузить ключи из файла
        with open("C:/Users/Airat/Desktop/lab3_PublicKey.txt", 'r', encoding='utf-8') as file:
            Key = ['','']
            index = 0
            tmp = []
            for i in file.read():
                if (i == ' '):
                    Key[index] = ''.join(str(tmp[j]) for j in range(len(tmp)))
                    index = 1
                    tmp = []
                else:
                    tmp.append(i)
            Key[index] = ''.join(str(tmp[j]) for j in range(len(tmp)))
        file.close()
        e = int(Key[0])
        n = int(Key[1])

    x, y, i, stage = random.randint(1,n-1), 1, 0, 2
    start = time.time()
    while(efclide(n,abs(x-y)) == 1):
        if (i == stage):
            y = x
            stage = stage * 2
        x = (x * x + 1) % n
        i = i + 1

    end = time.time()
    intervals.append((end - start))
    if (var.get() == False):
        keybit.append(int(key_len.get()))
    else:
        keybit.append(len(''.join(bin(n)[2:])))

    p = efclide(n,abs(x-y))
    q = int(n/p)
    eiler = (p - 1) * (q - 1)

    d = efclideEx(e, eiler)
    if (d < 0):
        d += eiler

    print(intervals)
    print(keybit)
    print("\nПодобранный ключ:")
    print(d)


def F(x,n):
    return ((x * x) - 1) % n


def fastPowNod(a,d,T):
    i = 1
    while(d>0):
        if(d % 2 != 0):
            i = i * a % T
        d = d // 2
        a = a * a % T
    return i

def fastPow(a,d):
    i = 1
    while(d>0):
        if(d % 2 != 0):
            i = i * a
        d = d // 2
        a = a * a
    return i


def efclide(a,b):
    while(b != 0):
        t = a % b
        a = b
        b = t
    return a


def efclideEx(m,n):
    a, b, u1, u2, v1, v2 = m, n, 1, 0, 0, 1
    while(b != 0):
        q = a // b
        r = a % b
        a = b
        b = r
        r = u2
        u2 = u1 - q * u2
        u1 = r
        r = v2
        v2 = v1 - q * v2
        v1 = r
    return u1


def numFerma(i):
    return fastPow(2,fastPow(2,i)) + 1


def numberGenerate(L):
    BitList = [random.getrandbits(1) for i in range(L)]
    BitList[0] = 1
    BitList[L - 1] = 1
    T = int(''.join(str(i) for i in BitList), 2)

    a = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
    i = 0
    while(i < 15):
        if(fastPowNod(a[i],T-1,T) != 1):
            i = 0
            BitList = [random.getrandbits(1) for i in range(L)]
            BitList[0] = 1
            BitList[L-1] = 1
            T = int(''.join(str(i) for i in BitList), 2)
        else: i += 1
    print("\nПростое число {} бит:".format(L))
    print(T)
    return T


def keyGenerate():
    l2.config(text='')
    if (key_len.get().isdigit()):
        L = int(key_len.get()) // 2
        l2.config(text="(Ключи длинной {} бит/битов сгенерированы)" .format(L*2))
    else:
        L = 128 // 2
        if(key_len.get() != ''):
            l2.config(text="(Некорректный формат введенных данных)")

    p = numberGenerate(L)
    q = numberGenerate(L)
    n = p * q
    eiler = (p - 1) * (q - 1)

    i = 4
    e = numFerma(i)
    while(efclide(eiler,e) != 1):
        e = numFerma(i)
        i += 1

    d = efclideEx(e, eiler)
    if(d < 0):
        d += eiler

    PublicKey = [e , n]
    PrivateKey = [d , n]

    print("\nPublicKey:")
    print(PublicKey)
    print("\nPrivateKey:")
    print(PrivateKey)

    with open("C:/Users/Airat/Desktop/lab3_PublicKey.txt", 'w', encoding='utf-8') as file:
        file.write(''.join(str(PublicKey[0])) + ' ' + ''.join(str(PublicKey[1])))
        file.close()
    with open("C:/Users/Airat/Desktop/lab3_PrivateKey.txt", 'w', encoding='utf-8') as file:
        file.write(''.join(str(PrivateKey[0])) + ' ' + ''.join(str(PrivateKey[1])))
        file.close()

    return e, n, d


global intervals, keybit
intervals = []
keybit = []

matplotlib.use('TkAgg')
root = Tk()
root.title("RSA")
root.geometry("990x500")
root.resizable(False, False)

canvas = Canvas(width=990, height=600, bg="#385773")\
    .place(x=-2,y=-2)

text1 = Text(width=60, height=20, bg="#A9C6D9", fg='#1C1C1C', wrap=WORD)
text1.place(x=4, y=4)
text2 = Text(width=60, height=20,bg="#A9C6D9", fg='#1C1C1C', wrap=WORD)
text2.place(x=500, y=4)

button1 = Button(root, width=25, height=2, text="Зашифровать файл", bg="#35648C", fg='#F2F2F0',
                 command=crypt)\
    .place(x=304, y=340)
button2 = Button(root, width=25, height=2, text="Расшифровать файл", bg="#35648C", fg='#F2F2F0',
                 command=deCrypt)\
    .place(x=500, y=340)
button3 = Button(root, width=25, height=2, text="Сгенерировать ключи", bg="#35648C", fg='#F2F2F0',
                 command=keyGenerate)\
    .place(x=304, y=430)
button4 = Button(root, width=25, height=2, text="p-эвристика", bg="#35648C", fg='#F2F2F0',
                 command=polardAttack)\
    .place(x=500, y=430)
button5 = Button(root, width=11, height=1, text="График T/b", bg="#35648C", fg='#F2F2F0',
                 command=RefreshGraf1)\
    .place(x=500, y=400)
button6 = Button(root, width=11, height=1, text="График T/r", bg="#35648C", fg='#F2F2F0',
                 command=RefreshGraf2)\
    .place(x=597, y=400)

key_len = StringVar()
entry = Entry(root, width=20, font=24, textvariable=key_len, bg="#35648C", fg='#F2F2F0')\
    .place(x=304, y=400)

var = BooleanVar()
var.set(0)
r1 = Radiobutton(root, text='Сгенерировать ключ', width=20, height=2,
                 value = 0, variable = var, bg="#6387A6").place(x=800, y=340)
r2 = Radiobutton(root, text='Загрузить ключ из файла', width=20, height=2,
                 value = 1, variable = var, bg="#6387A6").place(x=800, y=400)

l1 = Label(root, justify=RIGHT, text="Введите длину ключа в битах (по умолч. 128)", bg="#385773", fg='#F2F2F0')
l1.place(x=25, y=400)
l2 = Label(root, justify=RIGHT, text='', bg="#385773", fg='#F2F2F0')
l2.place(x=25, y=420)

# print(efclide(76451512,8733255912))
# print(pow(77,-1,13))
root.mainloop()