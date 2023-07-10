# Use TPM2 as FIDO token https://webauthn.io/

FROM

https://github.com/psanford/tpm-fido.git

FROM 

https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=tpm-fido-git

AND FROM

https://download.opensuse.org/source/tumbleweed/repo/oss/src/tpm-fido-20230621.5f8828b-1.1.src.rpm

```
rpmdev-setuptree
cd rpmbuild
rpmbuild -ba SPECS/tpm-fido.spec
```

![alt text](https://raw.githubusercontent.com/antnn/tpm-fido-rpm/058fc317219491ed97578d21da6fad7124bf17f3/Screenshot%20from%202023-07-10%2015-29-20.png)

