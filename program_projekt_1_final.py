import sys


## ----------------------------------------------
def main():
    '''funkcja główna programu'''
    print('Realizacja projektu nr 1 z Informatyki stosowanej II')
    fname = 'd201.txt'
    print(f'Analiza pliku danych: {fname}')

    X, Y = czytaj(fname)
##    pokaz( X, Y, open('sprawdzenie.txt', 'w'))
##    pokaz( X, Y)

    print(f'\n1. liczba punktów tabeli n = {len(X)}')
    print(f'   przedział zmienności x ε <{X[0]}, {X[-1]}>')
    print(f'   przedział wartości   y ε <{min(Y)}, {max(Y)}>')

    print('\n2. przedziały, w których funkcja jest:')
    przedzialy(X, Y, 'dodatnia', 'ujemna')
    
    Xprim, Yprim = pochodna( X, Y)
    Xbis, Ybis = pochodna( Xprim, Yprim)
    save2csv(X,Y,'funkcja.csv')
    save2csv(Xprim,Yprim,'pochodna.csv')
    save2csv(Xbis,Ybis,'druga pochodna.csv')

    przedzialy(Xprim, Yprim, 'rosnąca', 'malejąca')
    przedzialy(Xbis, Ybis, 'wypukła', 'wklęsła')

    txt = '\n3. liczba miejsc zerowych {}, ekstremów {}, punktów przegięcia {}'
    print(txt.format(liczba_zer(Y),
                     liczba_zer(Yprim),
                     liczba_zer(Ybis)))
    txt = '\n4. wartość funkcji w punkcie f({}) = {:.6f}'
    x = 4.674
    y = wartosc(x, X, Y)
    print(txt.format(x, y))

    txt = '\n5. wartość całki f(x) dla x = <{}, {}> = {:.6f}'
    print(txt.format(-1, 1, calka(-1,1,X,Y)))

    print('\n6. pierwiastki równania f(x) = 0 w przedziale objętym tabelą:')
    pierwiastki(X, Y)
    print('\n7. Wartość...')
    zadanie_7(Yprim)

    print('\n8. Zadanie nr 8')
    zadanie_8(Y)

## ----------------------------------------------
def zadanie_8(Y):
    counter = 0
    for y in Y:
        if (y < -0.5 and y > -1.0):
            counter += 1
    print(counter)

## ----------------------------------------------
def zadanie_7(Yprim):
    yp_max = -1
    for yp in Yprim:
        if abs(yp) > yp_max:
            yp_max = abs(yp)
    
    print(yp_max)


## ----------------------------------------------
def pierwiastki(X, Y):
    n = 0
    txt = 'x{} = {:.6f}, '
    txt_out = ''
    for i in range(len(X)-1):
        if Y[i] == 0:
            n += 1
            pierw = X[i]
            txt_out += txt.format(n, pierw)
        elif Y[i]*Y[i+1] < 0:
            n += 1
            pierw = met_siecznych(x0=X[i], x1=X[i+1], x2=X[i+2],
                                  y0=Y[i], y1=Y[i+1], y2=Y[i+2])
            txt_out += txt.format(n, pierw)
    print('   ' + txt_out[:-2])

## ----------------------------------------------
def calka(a:float, b:float, X:list, Y:list) -> float:
    def trap(x0,y0,x1,y1):
        return 0.5*(y0+y1)*(x1-x0)

    A = float(0)
    for i in range(len(X)-1):
        x0, x1 = X[i], X[i+1]
        y0, y1 = Y[i], Y[i+1]
        if a <= x0 and x1 <= b:
            A += trap(x0,y0,x1,y1)
        elif x0 < a and a < x1:
            A += trap(a, wartosc(a,X,Y), x1, y1)
        elif x0 < b and b < x1:
            A += trap(x0, y0, b, wartosc(b,X,Y))
    return A

## ----------------------------------------------
def wartosc(x, X, Y):
    for i in range(len(X)-2):
        if X[i] <= x and x < X[i+1]:
            return interpol_newton(x,
                                   X[i], Y[i],
                                   X[i+1], Y[i+1],
                                   X[i+2], Y[i+2])
    raise TypeError('Błąd interpolacji!')

## ----------------------------------------------
def liczba_zer(Y:list) -> int:
    n = 0
    for i in range(len(Y)-1):
        y0, y1 = Y[i], Y[i+1]
        if y0 == 0 or y0*y1 < 0:
            n += 1
    return n
    
## ----------------------------------------------
def pochodna(X, Y):
    xp, yp = [], []
    for i in range(len(X)-1):
        xi = 0.5*(X[i]+X[i+1])
        xp.append(xi)
        ir = (Y[i+1]-Y[i])/(X[i+1]-X[i])
        yp.append(ir)
    return xp, yp

## ----------------------------------------------
def interpol_newton(x, x0, y0, x1, y1, x2, y2):
    f01 = (y1-y0)/(x1-x0)
    f12 = (y2-y1)/(x2-x1)
    f012 = (f12-f01)/(x2-x0)
    return y0 + f01*(x-x0) + f012*(x-x0)*(x-x1)


## ----------------------------------------------
def przedzialy(X,Y,kom1,kom2):
    kom1 = f'   - {kom1: <10} '+ 'x ε <{:.3f}, {:.3f}>'
    kom2 = f'   - {kom2: <10} '+ 'x ε <{:.3f}, {:.3f}>'
    if Y[0] < 0:
        znak = -1 # wartości ujemne
    else:
        znak = 1 # wartości dodatnie
    start = X[0]
    for i in range(len(X)-1):
        stop = None
        if Y[i] == 0:
            stop = X[i]
        elif Y[i]*Y[i+1] < 0:
            stop = met_siecznych(X[i],  Y[i],
                                 X[i+1],Y[i+1],
                                 X[i+2],Y[i+2])
        if stop != None:
            if znak == 1:
                print(kom1.format(start,stop))
            else:
                print(kom2.format(start,stop))
            start = stop
            znak *= -1
    stop = X[-1]
    if znak == 1:
        print(kom1.format(start,stop))
    else:
        print(kom2.format(start,stop))
        
## ----------------------------------------------
def miejsce_zerowe(x0, y0, x1, y1):
    a = (y1-y0)/(x1-x0)
    b = y0 - a*x0
    return -b/a

def met_siecznych(x0, y0, x1, y1, x2, y2):
    xa, ya = x0, y0
    xb, yb = x1, y1
    eps = 1e-15

    while True:
        try:
            a = (yb-ya)/(xb-xa)
        except ZeroDivisionError:
            break
        b = ya - a*xa
        xc = -b/a
        yc = interpol_newton(xc, x0, y0, x1, y1, x2, y2)
        if abs(yc) < eps:
            break
        xa, ya = xb, yb
        xb, yb = xc, yc
    
    return (xa+xb)/2

def met_bisekcji(x0, y0, x1, y1, x2, y2):
    xa, ya = x0, y0
    xb, yb = x1, y1
    eps = 1e-12
    while xb - xa > eps:
        xc = (xa + xb)/2
        yc = interpol_newton(xc, x0, y0, x1, y1, x2, y2)
##        print( f'{xc = }')
        if yc*yb > 0:
            xb, yb = xc, yc
        else:
            xa, ya = xc, yc
    return (xa+xb)/2    

## ----------------------------------------------
def pokaz( warX, warY, plik=sys.stdout):
##    for i in range(len(warX)):
##        print(f'{warX[i]: >15} {warY[i]: >15}')
    for xi, yi in zip(warX, warY):
        print(f'{xi: >15}{yi: >15}', file=plik)
        

## ----------------------------------------------
def czytaj(nazwa_pliku):
    plik = open(nazwa_pliku, 'r')
    X, Y = [], []
    for line in plik:
        xi, yi = line.split()
        X.append( float(xi) )
        Y.append( float(yi) )
        
    return X, Y


def testowanie():
    x0, y0 = 0, -1
    x1, y1 = 3, 8
    x2, y2 = 4, 15
    print('Testowanie metody bisekcji...')
    print( met_bisekcji(x0, y0, x1, y1, x2, y2) )

    print('Testowanie metody siecznych...')
    print( met_siecznych(x0, y0, x1, y1, x2, y2) )

def save2csv(X, Y, fname):
    with open(fname, 'w') as file:
        for xi, yi in zip(X, Y):
            txt = f'{xi};{yi}'.replace('.', ',')
            print(txt, file=file)


## ----------------------------------------------
## uruchomienie programu
if __name__ == '__main__':
    main()
##    testowanie()
