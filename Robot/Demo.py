import rpa as r


r.init()
r.url('https://www.buda.com/ingreso')
r.type('318,50', 'eduardo.sinning@gmail.com[enter]')
#print(r.read('Web Results'))
r.snap('page', '../RPA/results.png')
r.close()