from mongoengine import *

connect('systemet2')

class Vara(Document):
    nr= StringField()
    Artikelid = StringField()
    Varunummer = StringField()
    Namn = StringField()
    Namn2 = StringField()
    Prisinklmoms = StringField()
    Volymiml = StringField()
    PrisPerLiter = StringField()


def load_file():
    testdata = open('testfil.txt','r', encoding='utf-8', errors='ignore')
    for rad in testdata:
        radlista = rad.split('\t')

        found_doc = Vara.objects(Artikelid=radlista[1])
        if not found_doc:
            newdoc = Vara(  
                nr=radlista[0],
                Artikelid=radlista[1],
                Varunummer=radlista[2],
                Namn=radlista[3],
                Namn2=radlista[4],
                Prisinklmoms=radlista[5],
                Volymiml=radlista[7],
                PrisPerLiter=radlista[8] 
                )
            newdoc.save()
        elif found_doc:
            if found_doc[0].Prisinklmoms != radlista[5]:
                print('Nytt Pris')
                print(str(found_doc[0]['Namn'])+', Prisförändring: '+(str(float(found_doc[0]['Prisinklmoms']) - float(radlista[5]))))
                found_doc.update(Prisinklmoms=radlista[5])
    testdata.close()
