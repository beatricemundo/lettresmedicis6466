# -*- coding: utf-8 -*-
import csv, glob, os, re, sys, time
from xml.dom import minidom

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))
# Open the input file
file = "Annexe chapitre I_balisé.txt"
inputFile = open(file, "r", encoding="utf-8")
outputFile = open(file+".xml", "w", encoding="utf-8")
documentLineNb = 0
letters = []
letter = {}
letter["id"] = ""
letter["text"] = ""
letter["date"] = ""
letter["source"] = ""
letter["destinataire"] = ""

def nettoieLigne(ligne):
   return ligne.replace("\r","").replace("\n","")

for line in inputFile:
   if line != "\n":
      line.replace("\n"," \n")
   res = re.search("^[0-9]+[.]LCM(02|10)[Mm]*[.]", line)
   if res:
      # Save former letter
      letter["text"] = '<discours loc="CathMed" date="' + letter["date"].replace(" ","").replace(".","") + '"><p>' + letter["text"].replace("  "," ") + "</p></discours>"
      letters.append(letter)
      # Prepare next letter
      documentLineNb = 0
      letter = {}
      letter["id"] = nettoieLigne(line)
      letter["text"] = ""
      letter["date"] = ""
      letter["source"] = ""
      letter["destinataire"] = ""
   if documentLineNb == 1 and line != "\n" :
      letter["date"] = nettoieLigne(line)
   if documentLineNb == 2 and line != "\n" :
      letter["source"] += " " + nettoieLigne(line)
   if documentLineNb == 3 and line != "\n" :
      letter["destinataire"] += " " + nettoieLigne(line)
   if documentLineNb < 4:
      # The line contains metadata about the letter
      if line != "\n" :
         if documentLineNb < 2 :
            documentLineNb += 1
      else:
         if documentLineNb == 2 and len(letter["source"]) > 0:
            documentLineNb = 3
         if documentLineNb == 3 and len(letter["destinataire"]) > 0:
            documentLineNb = 4
   else:
      # The line contains some text
      documentLineNb += 1
      if line == "\n":
         letter["text"] += "</p><p>"
      else:
         letter["text"] += " "
         previousEmptyLine = False
         letter["text"] += nettoieLigne(line)
         
letter["text"] = '<discours loc="CathMed" date="' + letter["date"].replace(" ","").replace(".","") + '"><p>' + letter["text"].replace("  "," ") + "</p></discours>"
letters.append(letter)

outputFile.writelines("<text>")
for letter in letters:
   smallOutputFile = open("data/" + letter["id"]+".xml", "w", encoding="utf-8")
   smallOutputFile.writelines("""<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="Teinte/teinte.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-stylesheet type="text/xsl" href="Teinte/tei2html.xsl"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="fr">
   <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Lettre """ + letter["id"] + """</title>
            <author key="Catherine de Médicis (1519-1589). Auteur du texte">Catherine de Médicis (1519-1589).</author>
            <funder><ref>Université Gustave Eiffel</ref></funder>
            <respStmt>
              <persName ref="#ND">Beatrice Mundo</persName>
              <resp><date>2023</date> Relecture du texte ; <date>2023</date> Encodage TEI</resp>
            </respStmt>
         </titleStmt>
         <publicationStmt>
            <publisher>Projet GP DIGIS, à partir du texte disponible sur Gallica (feuille de style issue du projet Teinte principalement développé par Frédéric Glorieux : https://github.com/oeuvres/Teinte)</publisher>
            <date when="2023"/>
            <availability status="free">
               <p>Licence ouverte version 2.0</p>
            </availability>
            <availability>
               <licence target="https://www.etalab.gouv.fr/licence-ouverte-open-licence/"/>
            </availability>            
         </publicationStmt>
         <sourceDesc>
            <bibl>
               <author>Catherine de Médicis (1519-1589). Auteur du texte</author>,
               <editor>Hector de La Ferrière</editor>,
               <title>Lettres de Catherine de Médicis. Tome 2 / publiées par M. le Cte Hector de la Ferrière,... [puis] par M. le Cte Baguenault de Puchesse,...</title>.
               <date>1885</date>,
               <publisher>Impr. nationale (Paris)</publisher>.
               <idno type="Gallica">https://gallica.bnf.fr/ark:/12148/bpt6k6228061d/</idno>
               <author>Catherine de Médicis (1519-1589). Auteur du texte</author>,
               <editor>Gustave Baguenault de Puchesse</editor>,
               <title>Lettres de Catherine de Médicis. Tome 10 / publiées par M. le Cte Hector de la Ferrière,... [puis] par M. le Cte Baguenault de Puchesse,...</title>.
               <date>1909</date>,
               <publisher>Impr. nationale (Paris)</publisher>.
               <idno type="Gallica">https://gallica.bnf.fr/ark:/12148/bpt6k6228018d/</idno>
            </bibl>
         </sourceDesc>
      </fileDesc>
      <profileDesc>
         <creation>
            <date when="1885">1885</date>
            <date when="1909">1909</date>
         </creation>
         <langUsage>
            <language ident="fr"/>
         </langUsage>
      </profileDesc>
   </teiHeader>
<text>
   """)
   outputFile.writelines(letter["text"].replace("<p></p>","").replace("<p","\n<p").replace("</discours>","\n</discours>").replace("<p>","  <p>")+"a a a a a a a a a a a a \n\n\n")
   smallOutputFile.writelines(letter["text"].replace("<p></p>","").replace("<p","\n<p").replace("</discours>","\n</discours>").replace("<p>","  <p>")+"\n\n\n")
   smallOutputFile.writelines("""
   </text>
</TEI>""")
   smallOutputFile.close()
outputFile.writelines("</text>")

outputFile.close()