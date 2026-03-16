# unisoc_secure_boot_bypass
A poc about bypassing unisoc's secure boot permanently and gaining EL3 code execution.

This vulnerability has been patched by Unisoc.
## Description

Unisoc's secure boot chain is like BOOTROM->SPL/FDL1->(TOS)->UBOOT/FDL2->KERNEL(For newer socs,POSTROM is added between BOOTROM and SPL)

BOOTROM verifies SPL correctly.

But for other verification,unisoc does not validate the image header.

There is a 0x200 byte-length image header on the top of the image.

It tells the payload len.

And at the end of the image ,located at 0x200+payload len offset,a cert header and a cert lie there.

The cert header tells the payload offset and payload len again.

And the verification logic only uses the payload offset and payload len in the cert header.

But the image loading function jumps to image load address + 0x200

So we can put the shellcode at 0x200 offset.And then put the original signed image after the shellcode.

And then change the payload offset at the cert header.

If you put the shellcode into TRUSTOS,you can gain EL3 code execution.
## DISCLAIMER

This is just a poc.

It is only for research and study.

I will not be responsible for any damage of your device and any abuse.
