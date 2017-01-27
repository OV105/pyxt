###############################################################################
#
# Copyright (c) 2009 Novell, Inc.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public License 
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact Novell, Inc.
#
# To contact Novell about this file by physical or electronic mail,
# you may find current contact information at www.novell.com
#
###############################################################################

BuildRequires: python-devel 

Name:         pyxt
License:      GPL 
Group:        Development/Tools/Other
Autoreqprov:  on
Version:      1.0
Release:      0
Summary:      Application for automating xwindows events.
Url:          http://www.novell.com 
Source:       %{name}-%{version}.tar.gz
#Patch:        %{name}-%{version}.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildArchitectures: noarch
#ExclusiveArch: %ix86
BuildRequires: python-devel
#Requires: rpm-python

%description
Tools for comparing lists of rpm packages. 
 
%prep 
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%setup  

%build
#python ./setup.py build
python ./setup.py build --debug

%install
#rm -rf $RPM_BUILD_ROOT
#python ./setup.py install -O2 --prefix="/usr" --root=$RPM_BUILD_ROOT --record=%{name}.files
python ./setup.py install --prefix="/usr" --root=$RPM_BUILD_ROOT --record=%{name}.files
sed -e 's/\.[0-9]$/&\*/' < %{name}.files > INSTALLED_FILES

%clean
#rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
#%{_bindir}/*
#%{python_sitelib}/%{name}
#%doc COPYING
#%doc NEWS
#%doc README
#%doc AUTHORS

#/usr/share/stasis
#/usr/bin/qa-xtest
#/usr/bin/qa-xtest-single
#/usr/bin/qa-log-replay
#/usr/lib/python2.4/site-packages/stasis
#/usr/share/doc/stasis

%changelog

