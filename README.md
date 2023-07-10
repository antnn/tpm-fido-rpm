#Use TPM2 as FIDO token https://webauthn.io/

FROM 

https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=tpm-fido-git

AND FROM

https://download.opensuse.org/source/tumbleweed/repo/oss/src/tpm-fido-20230621.5f8828b-1.1.src.rpm

```
rpmdev-setuptree
cd rpmbuild
rpmbuild -ba SPECS/tpm-fido.spec
```



