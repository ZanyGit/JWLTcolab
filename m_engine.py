# 
# Mongoengine är det paket som hanterar kopplingen till MongoDB 
from mongoengine import *

# Det här skapar en koppling till databasen 'systemet2' lokalt på din dator
connect('systemet2')


#Det här är en definition av hur ett dokument av typen Vara ser ut, jag har valt sju saker av de 30 som finns i filen
class Vara(Document):
    nr= StringField()
    Artikelid = StringField()
    Varunummer = StringField()
    Namn = StringField()
    Namn2 = StringField()
    Prisinklmoms = StringField()
    Volymiml = StringField()
    PrisPerLiter = StringField()

# det här monstret öppnar filen 'testfil.txt' sen läser den rad för rad och kollar först om artikelidt redan finns
# i databasen, gör den inte det så skapar den ett nytt dokument i databasen och sparar det. Finns det redan ett dokument 
# med samma artikelid så kollar den om priset i databasen är annat än det som är i textfilen, isf skriver den ut 
# diffen i consolfönstret, sedan sparas det nya värdet i databasen. Ifall priset är samma som i databasen går den bara vidare till nästa rad.

def load_file():
    testdata = open('testfil.txt','r', encoding='utf-8', errors='ignore')  # här kan du ändra namnet på den fil du vill öppna just nu är det 'testfil.txt'
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
