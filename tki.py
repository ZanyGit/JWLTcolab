from tkinter import *
from tkinter import filedialog
from mongoengine import *
import os
from PIL import Image, ImageTk


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
    root.filename = filedialog.askopenfilename(initialdir=dir_path, title="Select A File", filetypes=(("txt files","*.txt"),("All files","*.*")))
    testdata = open('testdata.txt','r', encoding='utf-8', errors='ignore')
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
                #print('Nytt Pris')
                message = str(found_doc[0]['Namn'])+', Prisförändring: '+(str(float(found_doc[0]['Prisinklmoms']) - float(radlista[5])))
                new_label = Label(root, text=message ).pack()
                #print(str(found_doc[0]['Namn'])+', Prisförändring: '+(str(float(found_doc[0]['Prisinklmoms']) - float(radlista[5]))))
                found_doc.update(Prisinklmoms=radlista[5])
    testdata.close()


dir_path = os.path.dirname(os.path.realpath(__file__))
connect('systemet2')
root = Tk()
root.title('Vinlistan')
my_img = ImageTk.PhotoImage(Image.open('vingubbe.png'))
img_label = Label(root,image=my_img)
img_label.image = my_img
img_label.pack()
load_btn = Button(root, text="Load file", command=load_file).pack()


root.mainloop()




