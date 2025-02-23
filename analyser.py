# Projet_reseaux:





def OffsetValide(OffsetCourant, OffsetPrecedant):
    """Cette fonction compare les deux arguments renvoie True si le premier est superieur au deuxieme Offset . 
    Arguments : 1)-> Offset courant,
                       2)-> Offset precedant.
    Retourne : True si l'Offset courant est valide c'est à dire si il est superieur à l'Offset  precedant)
    """
    try:
        Offs = int(OffsetCourant, 16) 																#L'offset en hexadecimal
    except:
        return False
    
    if Offs == 0 :
        return True
    
    return Offs >= OffsetPrecedant 
    

def SequenceOctetValide(SequenceOctet, NmbrOctets): 
    """Cette fonction lit la sequences d'octets passée en arguments .
    Arguments : 1)-> Sequence d'octets,
    				   2)->  Nombre d'octets.
    Retourne : True si tous les nombres d'octets sont des caracteres hexadecimaux, False sinon
    """
    fin = False
    indd = 0
    
    while not fin :
        if NmbrOctets == 0 :
            return True
        try:
            int(SequenceOctet[indd], 16)                                                                                          #Recuperation de l'offset en position indd 
        except:
            return False

        indd+=1
        NmbrOctets-=1

#-------------------------------------------------------------------------------------------Couche 02:Ethernet-----------------------------------------------------------------------------------------------------

def Ethernet (Trame) : 
    """Cette fonction analyse la Trame Ethernet  et affiche ses champs 
    Argument : Trame à analyser
    """
    TypeDeProtocol = {"0800": "IPVersion4", "0805": "X.25 niveau 3", "0806" : "ARP"}
    
    AdrDestination = Trame[0]+":"+Trame[1]+":"+Trame[2]+":"+Trame[3]+":"+Trame[4]+":"+Trame[5]
    AdrSource = Trame[6]+":"+Trame[7]+":"+Trame[8]+":"+Trame[9]+":"+Trame[10]+":"+Trame[11]
    
    typee = Trame[12]+Trame[13]
    
    print("   "+Colors.BOLD+Colors.UNDERLINE+"Protocol Ethernet:"+Colors.ENDC)
    print("\tDestination: {}".format(AdrDestination))
    print("\tSource: {}".format(AdrSource))

    if(typee in TypeDeProtocol.keys()):
    
        print("\tType: {} (0x{}) ".format(TypeDeProtocol[typee], typee))
        outputFile.write("\tType: {} (0x{}) \n".format(TypeDeProtocol[typee], typee))
    
    outputFile.write("   Protocol Ethernet:\n")
    outputFile.write("\tDestination: {}\n".format(AdrDestination))
    outputFile.write("\tSource: {}\n".format(AdrSource))
   
    if typee == "0800":
        IPVersion4(Trame)
    
    elif typee == "0806":
        ARP(Trame)
    
    else :
        print(Colors.WARNING+Colors.BOLD+"  Protocol numéro {} non supporté".format(typee)+Colors.ENDC)
        outputFile.write("  Protocol numéro {} non supporté\n".format(typee))


def Couches (Dico):
    
    Trames = Dico["trames correctes"]
    NmbrTrames = len(Trames)
    
    print(Colors.FAIL+Colors.BOLD+"Le nombre de trames erronees est : " + str(len(Dico["trames erronees"])) + Colors.ENDC)
    outputFile.write("Le nombre de trames erronees est : " + str(len(Dico["trames erronees"]))+"\n")

    for ligne in Dico["lignes erronees"]:
        print("\tLigne numero {} erronnée ou imcomplète".format(ligne))
        outputFile.write("\tLigne numero {} erronnée ou imcomplète\n".format(ligne))

    print(Colors.OKGREEN+Colors.BOLD+"Le nombre de trames correctes est : "+ str(NmbrTrames)+ Colors.ENDC+"\n")
    outputFile.write("Le nombre de trames correctes est : "+ str(NmbrTrames)+"\n"+"\n")

    for Trame, i  in zip(Trames, range(len(Trames))) :
        print(Colors.WARNING+"Trame numero {} : -- {} octets --".format(i, len(Trame))+Colors.ENDC)
        outputFile.write("Trame {} : -- {} octets --\n".format(i, len(Trame)))
        try :
            Ethernet(Trame)
        except Exception as excep:
            if hasattr(excep, 'message'):
                print(excep.message)
            else:
                print(excep)
            
        print("\n")
        outputFile.write("\n")

def ARP (Trame):
    """Cette fonction analyse le datagramme ARP et ses champs
    Argument : Trame à analyser
    type du Hardware est Ethernet
                 type du protocole est IPVersion4
    """
    print("   "+Colors.BOLD+Colors.UNDERLINE+"Adress Resolution Protocol:"+Colors.ENDC)
    outputFile.write("   Adress Resolution Protocol:\n")
    
    Offset = 14  
    
    Hardware = Trame[Offset]+Trame[Offset+1]
    Protocol = Trame[Offset+2]+Trame[Offset+3]
    
    Hardlen = Trame[Offset+4]
    Protlen = Trame[Offset+5]
    
    Operation =  Trame[Offset+6]+Trame[Offset+7]
    
    Sha =  Trame[Offset+8]+":"+Trame[Offset+9]+":"+Trame[Offset+10]+":"+Trame[Offset+11]+":"+Trame[Offset+12]+":"+Trame[Offset+13]
    Spa =  ".".join([str(int(oc, 16)) for oc in Trame[Offset+14:Offset+18]])
    Tha =  Trame[Offset+18]+":"+Trame[Offset+19]+":"+Trame[Offset+20]+":"+Trame[Offset+21]+":"+Trame[Offset+22]+":"+Trame[Offset+23]
    Tpa =  ".".join([str(int(oc, 16)) for oc in Trame[Offset+24:Offset+28]])

    if   int(Hardware,16) == 1:  
        print("\tHardware type: Ethernet (1)")
        outputFile.write("\tHardware type: Ethernet (1)\n")
        
    if Protocol == "0800":
        print("\tProtocol type: IPVersion4 (0x0800)") 
        outputFile.write("\tProtocol type: IPVersion4 (0x0800)\n")


    print("\tHardware size: {}".format(int(Hardlen,16)))
    outputFile.write("\tHardware size: {}\n".format(int(Hardlen,16)))

    print("\tProtocol size: {}".format(int(Protlen,16)))
    outputFile.write("\tProtocol size: {}\n".format(int(Protlen,16)))

    Opcode = {"0001" : "request (1)", "0002" : "reply (2)"}
    print("\tOpcode: {}".format(Opcode[Operation]))

    outputFile.write("\tOpcode: {}\n".format(Opcode[Operation]))
    print("\tSender Hardware address: {}".format(Sha))

    outputFile.write("\tSender Hardware address: {}\n".format(Sha))
    print("\tSender Protocol adress: {}".format(Spa))

    outputFile.write("\tSender Protocol adress: {}\n".format(Spa))
    print("\tTarget Hardware address: {}".format(Tha))

    outputFile.write("\tTarget Hardware address: {}\n".format(Tha))
    print("\tTarget Protocol adress: {}".format(Tpa))
    outputFile.write("\tTarget Protocol adress: {}\n".format(Tpa))

#------------------------------------------------------------------------------------------------------Couches 3: IP--------------------------------------------------------------------------------------------------

def IPVersion4(Trame):
    """Cette fonction analyse le datagramme IP version 4  affiche ses champs
    Argument : Trame à analyser
    """
    
    Offset = 14                                                                                #Début du datagramme IPVersion4 par rapport au début de la Trame
    Protocols= {1: "ICMP", 2 : "IGMP", 6 : "TCP", 17: "UDP", 36 : "XTP"}

    Version = Trame[Offset+0][0]

    HeaderLength32 = int(Trame[Offset+0][1], 16)  

    if HeaderLength32<5 :
        raise ValueError("	La Valeur minimum du header IP est 20 octets.")

    Tos =  Trame[Offset+1]

    TotalLength = Trame[Offset+2]+Trame[Offset+3]
    

    Identification = Trame[Offset+4]+Trame[Offset+5]
    FirstByte = format(int(Trame[Offset+6], 16), '08b')
    SecondByte = format(int(Trame[Offset+7], 16), '08b')
    ReservedBit = FirstByte[0]
    DoNotFragment = FirstByte[1]
    MoreFragment = FirstByte[2]
    FragmentOffset = FirstByte[3:]+SecondByte

    Ttl = Trame[Offset+8]
    Protocol = int(Trame[Offset+9], 16)
    
    HeaderChecksum =Trame[Offset+10]+Trame[Offset+11]
    
    Source_addr= '.'.join([str(int(x,16)) for x in Trame[Offset+12:Offset+16]])
    Dest_addr='.'.join([str(int(x,16)) for x in Trame[Offset+16:Offset+20]])
    
    OptionsType = 1

    print("   "+Colors.BOLD+Colors.UNDERLINE+"Internet Protocol Version 4:"+Colors.ENDC)
    print("\t{} .... = Version: 4 ".format(format(int(Version, 16), '04b')))
    print("\t.... {} = Header Length: {} bytes ({}) ".format(format(int(str(HeaderLength32), 16), '04b'),int(str(HeaderLength32),16)*4,HeaderLength32))
    print("\tIdentification: 0x{} ({})".format(Identification,int(Identification,16)))

    Dic_not_set={"0":"Not set","1":"Set"}

    print("\tFlags: 0x{} ".format(Trame[Offset+6]))
    print("\t\t{}... .... = Reserved bit: {} ".format(ReservedBit,Dic_not_set[ReservedBit]))
    print("\t\t.{}.. .... = Don't fragment: {} ".format(DoNotFragment,Dic_not_set[DoNotFragment]))
    print("\t\t..{}. .... = More fragments: {} ".format(MoreFragment,Dic_not_set[MoreFragment]))
    print("\tTotal Length: {}".format(int(TotalLength,16)))
    print("\tTime to Live: {}".format(int(Ttl,16)))

    if(Protocol in Protocols.keys()):
        print("\tProtocol: {} ({})".format(Protocols[Protocol],Protocol))
        outputFile.write("\tProtocol: {} ({})\n".format(Protocols[Protocol],Protocol))

    print("\tHeader Checksum: 0x{}".format(HeaderChecksum))
    print("\tSource Address: {}".format(Source_addr))
    print("\tDestination Address: {}".format(Dest_addr))


    outputFile.write("   Internet Protocol Version 4:\n")
    outputFile.write("\t{} .... = Version: 4 \n".format(format(int(Version, 16), '04b')))
    outputFile.write("\t.... {} = Header Length: {} bytes ({}) \n".format(format(int(str(HeaderLength32), 16), '04b'),int(str(HeaderLength32),16)*4,HeaderLength32))
    outputFile.write("\tIdentification: 0x{} ({})\n".format(Identification,int(Identification,16)))
    outputFile.write("\tFlags: 0x{} \n".format(Trame[Offset+6]))
    outputFile.write("\t\t{}... .... = Reserved bit: {} \n".format(ReservedBit,Dic_not_set[ReservedBit]))
    outputFile.write("\t\t.{}.. .... = Don't fragment: {} \n".format(DoNotFragment,Dic_not_set[DoNotFragment]))
    outputFile.write("\t\t..{}. .... = More fragments: {} \n".format(MoreFragment,Dic_not_set[MoreFragment]))
    outputFile.write("\tTotal Length: {}\n".format(int(TotalLength,16)))
    outputFile.write("\tTime to Live: {}\n".format(int(Ttl,16)))
    outputFile.write("\tHeader Checksum: 0x{}\n".format(HeaderChecksum))
    outputFile.write("\tSource Address: {}\n".format(Source_addr))
    outputFile.write("\tDestination Address: {}\n".format(Dest_addr))

#-----------------------------------------------------------------------------------------------------OPTIONS IP-----------------------------------------------------------------------------------------------------

    
    if (HeaderLength32 > 5):                                                                     #Si la longueur >20Bytes alors le Header IP contiens des otpions 

        NmbrOctetsOptions = (HeaderLength32 - 5) * 4
        print("\tOptions: {} bytes".format(NmbrOctetsOptions))

        outputFile.write("\tOptions: {} bytes\n".format(NmbrOctetsOptions))

        off = Offset+20

        while True : 
            if NmbrOctetsOptions == 0 : 
                break
            PremierOctetOption = Trame[off]                                                #Champ type de l'option

            if (int(PremierOctetOption, 16) == 0):
                print("\t  IP Option  -  End of Options List (EOL)")
                outputFile.write("\t  IP Option  -  End of Options List (EOL)\n")
                print("\t\tType: 0")
                outputFile.write("\t\tType: 0\n")
                off+=1
                NmbrOctetsOptions -=1
            elif (int(PremierOctetOption, 16) == 1):
                print("\t  IP Option  -  No Operation (NOP)")
                outputFile.write("\t  IP Option  -  No Operation (NOP)\n")
                print("\t\tType: 1")
                outputFile.write("\t\tType: 1\n")
                off+=1
                NmbrOctetsOptions -=1
            elif (int(PremierOctetOption, 16) == 7):
                print("\t  IP Option  -  Record Route (RR)")
                outputFile.write("\t  IP Option  -  Record Route (RR)\n")

                print("\t\tType: 7")
                outputFile.write("\t\tType: 7\n")

                Length = int(Trame[off+1], 16)
                print("\t\tLength: {}".format(Length))

                outputFile.write("\t\tLength: {}\n".format(Length))

                Pointer = int(Trame[off+2], 16)

                print("\t\tPointer: {}".format(Pointer))
                outputFile.write("\t\tPointer: {}\n".format(Pointer))

                for i in range((Length-3)//4):
                    RR= '.'.join([str(int(x,16)) for x in Trame[off+3+i*4:off+7+i*4]])
                    print("\t\tRecorded Route: {}".format(RR))
                    outputFile.write("\t\tRecorded Route: {}\n".format(RR))
                
                off+=Length
                NmbrOctetsOptions -= Length

            elif (int(PremierOctetOption, 16) == 131):
                print("\t  IP Option  -  Loose Source Route (LSR)")
                outputFile.write("\t  IP Option  -  Loose Source Route (LSR)\n")

                print("\t\tType: 131")
                outputFile.write("\t\tType: 131\n")

                Length = int(Trame[off+1], 16)
                print("\t\tLength: {}".format(Length))
                outputFile.write("\t\tLength: {}\n".format(Length))
                Pointer = int(Trame[off+2], 16)

                print("\t\tPointer: {}".format(Pointer))
                outputFile.write("\t\tPointer: {}\n".format(Pointer))

                for i in range((Length-3)//4):
                    Route= '.'.join([str(int(x,16)) for x in Trame[off+3+i*4:off+7+i*4]])
                    print("\t\tRoute: {}".format(Route)) 
                    outputFile.write("\t\tRoute: {}\n".format(Route))
                off+=Length
                NmbrOctetsOptions -= Length

            elif (int(PremierOctetOption, 16) == 137):
                print("\t  IP Option  -  Strict Source Route (SSR)")
                outputFile.write("\t  IP Option  -  Strict Source Route (SSR)\n")

                print("\t\tType: 137")
                outputFile.write("\t\tType: 137\n")
                Length = int(Trame[off+1], 16)

                print("\t\tLength: {}".format(Length))
                outputFile.write("\t\tLength: {}\n".format(Length))
                Pointer = int(Trame[off+2], 16)

                print("\t\tPointer: {}".format(Pointer))
                outputFile.write("\t\tPointer: {}\n".format(Pointer))

                for i in range((Length-3)//4):
                    Route= '.'.join([str(int(x,16)) for x in Trame[off+3+i*4:off+7+i*4]])
                    print("\t\tRoute: {}".format(Route)) 
                    outputFile.write("\t\tRoute: {}\n".format(Route)) 
                off+=Length
                NmbrOctetsOptions -= Length

            elif (int(PremierOctetOption, 16) == 148):
                print("\t  IP Option  -  Router Alert ")
                outputFile.write("\t  IP Option  -  Router Alert \n")
                print("\t\tType: 148")
                outputFile.write("\t\tType: 148\n")
                Length = int(Trame[off+1], 16)
                print("\t\tLength: {}".format(Length))
                outputFile.write("\t\tLength: {}\n".format(Length))
                RouterAlert = int(Trame[off+2]+Trame[off+3], 16)
                print("\t\tRouter Alert: Router shall examine packet ({})".format(RouterAlert))
                outputFile.write("\t\tRouter Alert: Router shall examine packet ({})\n".format(RouterAlert))
                off+=Length
                NmbrOctetsOptions -= Length
            else:
                print("\t  IP Option non supporté ")    # Toutes les options qui ne sont pas supportées ont un champs longueur
                outputFile.write("\t  IP Option non supporté \n")
                Length = int(Trame[off+1], 16)
                off+=Length
                NmbrOctetsOptions -= Length
    if (Protocol == 6):
        
        TCP(Trame,int(HeaderLength32)*4)

    elif Protocol == 17 : 
        UDP(Trame,int(HeaderLength32)*4)

    else:
        print("   "+Colors.BOLD+Colors.UNDERLINE+"Protocol numéro {} non supporté".format(Protocol)+Colors.ENDC)
        outputFile.write("   Protocol numéro {} non supporté\n".format(Protocol))

#----------------------------------------------------------------------------------------------Couche04: UDP--------------------------------------------------------------------------------------------------------

def UDP (Trame, LongueurIP):
    """Cette fonction analyse le segment UDP affiche ses champs
    Arguments :1)-> Trame à analyser,
    				  2)-> Longueur de l'entete IP
    """
    Offset = 14+LongueurIP 

    Source_port=Trame[Offset]+Trame[Offset+1]
    Dest_port=Trame[Offset+2]+Trame[Offset+3]

    Length = Trame[Offset+4]+Trame[Offset+5]
    Checksum = Trame[Offset+6]+Trame[Offset+7]

    print("   "+Colors.BOLD+Colors.UNDERLINE+"User Datagram Protocol: (UDP)"+Colors.ENDC)

    print("\tSource Port: {}".format(int(Source_port,16)))
    outputFile.write("\tSource Port: {}".format(int(Source_port,16)))

    print("\tDestination Port : {}".format(int(Dest_port,16)))
    outputFile.write("\tDestination Port : {}".format(int(Dest_port,16)))

    print("\tLength: {}".format(int(Length,16)))
    outputFile.write("\tLength: {}".format(int(Length,16)))

    print("\tChecksum: 0x{} [unverified]".format(Checksum))
    outputFile.write("\tChecksum: 0x{} [unverified]".format(Checksum))


#---------------------------------------------------------------------------------------------ParseFile----------------------------------------------------------------------------------------------------------------

def FichierParse (file):
    """Cette fonction lit le fichier qui contenant les trames à analyser.
    Argument :  un fichier dans le meme repertoire.
    Retourne  un dictionnaire des trames correctes et de trames erronees et les lignes qui sont fausses dans les trames erronees .
    
    """
    OffsetCourant = 0

    Lignes = file.readlines()

    LignesValides, PositionLignes = [], {}
    

    for index in range(len(Lignes)):

        Ligne = Lignes[index].strip().lower() 														#On enleve les espaces à gauche et à droite puis mettre les caracteres en minuscule

        if Ligne :
            Offset = Ligne.split(maxsplit=1)[0] 																						#Lecture  de l'offset du debut de ligne
        else:
            Offset = ""

        if OffsetValide(Offset, OffsetCourant):
            OffsetCourant = int(Offset, 16)
            PositionLignes[Ligne] = index
            LignesValides.append(Ligne) 																								#On ajoute l'offset dans le tableau ssi il est valide
        else:
            print("Ligne removed  :  ", Lignes[index])

    TramesCorrectes = []
    TramesErronees = []
    LignesErronees = []

    for index in range(len(LignesValides)):

        OffsetCourant = int(LignesValides[index].split(maxsplit=1)[0], 16)
        if index+1 == len(LignesValides) : 
            OffsetSuivant = 0
        else:
            OffsetSuivant = int(LignesValides[index+1].split(maxsplit=1)[0], 16)

        if OffsetCourant == 0:
            Trame = []
            trameValide = True
        
        splittedLine = LignesValides[index].split()

        if OffsetSuivant != 0 :
            NmbrOctetsSurLaLigne = OffsetSuivant - OffsetCourant

            if SequenceOctetValide(splittedLine[1:], NmbrOctetsSurLaLigne) : 
                Trame.extend(splittedLine[1:NmbrOctetsSurLaLigne+1])
            else:
                LignesErronees.append(PositionLignes[LignesValides[index]])
                trameValide = False
        else: 
            

            if Trame[12]+Trame[13] == "0806":   
                LongueurTrame = 60-14         
            else :
                if len(Trame) > 18:  
                    LongueurTrame = int(Trame[16]+Trame[17], 16)
                else:
                    LongueurTrame = -1
                    if len(splittedLine[1:]) > 18 - len(Trame) :  
                        try:
                            LongueurTrame = int(splittedLine[17-len(Trame)]+splittedLine[18-len(Trame)], 16)
                        except: 
                            trameValide = False
                            LignesErronees.append(PositionLignes[LignesValides[index]])
                            print("Champs longueur totale du datagramme IP érroné ligne erronée : numéro :", PositionLignes[LignesValides[index]])
            NmbrOctetsSurLaLigne = LongueurTrame + 14 - len(Trame)     									#LongueurTrame représente la longueur totale de la Trame
                                                                    																			     
            if SequenceOctetValide(splittedLine[1:], NmbrOctetsSurLaLigne) :
                print(splittedLine[1:NmbrOctetsSurLaLigne+1])
                Trame.extend(splittedLine[1:NmbrOctetsSurLaLigne+1])
            else:
                trameValide = False
                LignesErronees.append(PositionLignes[LignesValides[index]])

            if trameValide :
                TramesCorrectes.append(Trame)
            else:
                TramesErronees.append(Trame)

    return {"trames correctes" : TramesCorrectes,
            "trames erronees" : TramesErronees,
            "lignes erronees" : LignesErronees,
            }

#---------------------------------------------------------------------------------------------Couche07: DHCP&DNS------------------------------------------------------------------------------------------------

class Colors:
	OKGREEN = '\033[92m'
	UNDERLINE = '\033[4m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	ENDC = '\033[0m'

outputFile = open("resultatAnalyseur.txt", "w")

def main():
    while True:
        fileName = input(Colors.BOLD+"Entrer le nom du fichier contenant la(les) Trame(s) : "+Colors.ENDC)
        try:
            file = open(fileName)
        except:
            print("Fichier non existant !! ")
        else:
            break
    outputFile.write("Trame(s) extraite(s) du fichier : "+fileName+"\n")
    Dico = FichierParse(file)
    Couches(Dico)
    outputFile.close()


if __name__ == "__main__":
    main()



 
