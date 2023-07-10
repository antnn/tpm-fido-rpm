#
# spec file for package tpm-fido
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

# Prepare sources and vendor bundle with: osc service mr

Name:           tpm-fido
Version:        20230621.5f8828b
Release:        1.1
Summary:        Use your TPM2 as a FIDO 2FA token
License:        MIT
URL:            https://github.com/psanford/tpm-fido
Source:         %{name}-%{version}.tar.gz
Source1:        vendor.tar.zstd
Source2:        tpm-fido.rules
Source3:        tpm-fido.service
BuildRequires:  golang
BuildRequires:  zstd
Requires:       pinentry-gui
Provides:       tpm2-fido

%define debug_package %{nil}

%description
tpm-fido is FIDO token implementation for Linux that protects the token keys by using your system's TPM. tpm-fido uses Linux's uhid facility to emulate a USB HID device so that it is properly detected by browsers.

%prep
%autosetup -p1 -a1

%build
go build \
   -mod=vendor \
   -buildmode=pie

%install
install -D -m0755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m0644 $RPM_SOURCE_DIR/tpm-fido.rules %{buildroot}%{_prefix}/lib/udev/rules.d/99-tpm-fido.rules
install -D -m0644 $RPM_SOURCE_DIR/tpm-fido.service %{buildroot}%{_prefix}/lib/systemd/user/tpm-fido.service
install -D -m0644 $RPM_SOURCE_DIR/tpm-fido.sysusers %{buildroot}%{_prefix}/lib/sysusers.d/tpm-fido.conf
install -D -m0644 $RPM_SOURCE_DIR/uhid.conf %{buildroot}/etc/modules-load.d/uhid.conf


%files
%license LICENSE
%doc Readme.md
%{_bindir}/%{name}
%{_prefix}/lib/udev/rules.d/99-tpm-fido.rules
%{_prefix}/lib/systemd/user/tpm-fido.service
%{_prefix}/lib/sysusers.d/tpm-fido.conf
/etc/modules-load.d/uhid.conf

%post
printf "To use tpm-fido, add your user to the tss group and run:\n"
printf "systemctl --user enable --now tpm-fido.service\n"

%changelog
* Fri Jun 23 2023 dheidler@suse.de
- Update to version 20230621.5f8828b:
  * Add build/test workflow
  * Fix builds on 32bit architectures
* Tue Jun 20 2023 Jeff Kowalczyk <jkowalczyk@suse.com>
- Add BuildRequires: golang(API) >= 1.16 (min version per go.mod)
  This or metapackage BuildRequires: go are recommended to pull in
  the Go toolchain.
- Drop Requires: golang-packaging. The original macros for file
  movements into GOPATH are obsolete with Go modules. Macro
  go_nostrip is no longer needed with current binutils and Go.
- Remove manual call to strip the binary. Go binaries are stripped
  automatically in the default configuration.
  Refs boo#1210938
  * GNU strip circa 2016 would incorrectly strip Go intermediate
    step .a binaries (which are not .a ar archives) and write out
    an invalid binary instead of erroring on unrecognized format.
  * Error manifested in Go applications as fmt.a: go archive is
    missing __.PKGDEF on OBS built Go binaries which had passed
    their binary build step but fail at debuginfo creation step
    (which involves binary stripping).
  * The primary use of Go intermediate step .a binaries was for a
    precompiled standard library cache. The .a files comprised
    large fraction of the on-disk <go1.20 toolchain package size.
  * go1.20+ now use the normal Go build cache for the Go standard
    library. Go intermediate step .a archives are no longer part of
    the regular build process and not affected by GNU strip
    misidentifying them as ar archives.
    https://go.dev/doc/go1.20#go-command
- Use _service mode manual as better alias name than disabled
* Mon Jun 19 2023 Dominik Heidler <dheidler@suse.de>
- Initial Packaging
