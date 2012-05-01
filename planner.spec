%ifarch s390 s390x
%define build_eds_backend 0
%else
%define build_eds_backend 1
%endif

Summary:   A graphical project management tool
Name:      planner
Version:   0.14.4
Release:   9%{?dist}
License:   GPLv2+
Group:     Applications/Productivity
URL:       http://live.gnome.org/Planner
Source0:   http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.14/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gtk2-devel >= 2.2.0, libgnomeui-devel >= 2.0.1 
BuildRequires: libglade2-devel >= 2.0.0, gnome-vfs2-devel >= 2.0.2
BuildRequires: libgnomeprintui22-devel >= 2.2.0, libxml2-devel >= 2.5.4
BuildRequires: libxslt-devel >= 1.0.27, libgsf-devel, gtk-doc, pygtk2-devel
BuildRequires: scrollkeeper, glib2-devel, python-devel, intltool, autoconf
BuildRequires: automake, libtool, evolution-data-server-devel >= 1.9.1
%if %{build_eds_backend}
BuildRequires: evolution-devel >= 2.9.1
%endif
Requires:  shared-mime-info
Requires(post): %{_bindir}/scrollkeeper-update
Requires(postun): %{_bindir}/scrollkeeper-update

Patch0: planner-gnome349304-recentlyused.patch
Patch1: planner-gnome596173-xdg.patch
Patch2: planner-gnome596966-editoninsert.patch
Patch3: planner-gnome550559-fitzoom.patch
Patch4: planner-buildfix.patch
Patch5: planner-gnome603693-planner-calendar-for-edittask.patch
Patch6: planner-gnome604169-comboboxentry.patch
Patch7: planner-gnome604355-scrolling.patch

%description
Planner is a visual project management application which allows users to
manage several aspects of a project, including schedule tracking using
Gantt charts.

You should install Planner if you wish to manage schedules, allocate
resources, and track the progress of your projects.

%package devel
Summary: Libraries and include files for developing with planner
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig, glib2-devel, libxml2-devel, libgsf-devel

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with planner.

%package eds
Summary: Planner integration with evolution
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description eds
This package provides a plugin to integration planner and evolution.

%prep
%setup -q
%patch0 -p1 -b .recentlyused
%patch1 -p1 -b .xdg
%patch2 -p1 -b .editoninsert
%patch3 -p1 -b .fitzoom
%patch4 -p1 -b .buildfix
%patch5 -p1 -b .edittask
%patch6 -p1 -b .combobox
%patch7 -p1 -b .scrolling

%build
rm -rf libegg
autoreconf -f -i
%if %{build_eds_backend}
%define eds_backend_flags --enable-eds-backend
%else
%define eds_backend_flags --disable-eds-backend
%endif
%configure --enable-python --disable-gtk-doc --disable-dotnet --disable-update-mimedb %{eds_backend_flags} --enable-eds --disable-static
make # %{?_smp_mflags} not parallel build safe

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT/var/scrollkeeper
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/file-modules/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/storage-modules/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/views/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/gtk-2.0/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/storage-modules/libstorage-sql*
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/libsql-plugin*
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution-data-server-1.2/extensions/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/evolution/*/plugins/*.la

%if %{build_eds_backend}
pushd $RPM_BUILD_ROOT/%{_libdir}/evolution-data-server-1.2/extensions
rm -f libecalbackendplanner.so
rm -f libecalbackendplanner.so.0
mv -f libecalbackendplanner.so.0.0.0 libecalbackendplanner.so
popd
%endif

rm -f $RPM_BUILD_ROOT/%{_datadir}/mime/XMLnamespaces
rm -f $RPM_BUILD_ROOT/%{_datadir}/mime/globs
rm -f $RPM_BUILD_ROOT/%{_datadir}/mime/magic
rm -f $RPM_BUILD_ROOT/%{_datadir}/mime/application/*
rm -f $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}/*.sql
rm -f $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}/*.planner

%find_lang %{name}

%post
/sbin/ldconfig
scrollkeeper-update
if (update-mime-database -v &> /dev/null); then
    update-mime-database "%{_datadir}/mime" > /dev/null
fi

%postun
/sbin/ldconfig
scrollkeeper-update
if (update-mime-database -v &> /dev/null); then
    update-mime-database "%{_datadir}/mime" > /dev/null
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog NEWS README COPYING examples/*.planner
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/file-modules
%{_libdir}/%{name}/storage-modules
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/libhtml-plugin.so
%{_libdir}/%{name}/plugins/libmsp-plugin.so
%{_libdir}/%{name}/plugins/libxmlplanner-plugin.so
%{_libdir}/lib%{name}-1.so.*
%{_libdir}/python*/site-packages/*.so
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/48x48/mimetypes/*.png
%{_datadir}/mime/packages/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/gnome/help/%{name}/*
%{_datadir}/omf/%{name}/%{name}-*.omf
%{_mandir}/man1/planner.1.gz

%files eds
%defattr(-,root,root,-)
%{_libdir}/%{name}/plugins/libeds-plugin.so
%if %{build_eds_backend}
%{_libdir}/evolution-data-server-1.2/extensions/libecalbackendplanner.so
%{_libdir}/evolution/*/plugins/liborg-gnome-planner-source.so
%{_libdir}/evolution/*/plugins/org-gnome-planner-source.eplug
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1.0
%{_libdir}/lib%{name}-1.so
%{_datadir}/gtk-doc/html/lib%{name}
%{_libdir}/pkgconfig/*

%changelog
* Thu Jan 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.14.4-9
- Resolves: rhbz#557211 evolution is excluded from s390/s390x

* Fri Dec 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-8
- Resolves: rhbz#546515 allow scrolling

* Wed Dec 09 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-7
- Resolves: rhbz#545711 use GtkComboBoxEntry instead of GtkCombo

* Thu Dec 03 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-6
- Resolves: rhbz#543741 use PlannerCalander in edit->task

* Mon Nov 23 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-5
- Resolves: rhbz#540242 fix gtk_recent_manager_add_full usage

* Tue Nov 17 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-4
- Resolves: rhbz#526295 automatically go to edit mode on insert task
- Resolves: rhbz#537854 fix zoom to fit

* Thu Sep 24 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-3
- Resolves: rhbz#524662 Implement new Gnome XDG Config Folders for planner
    + gnome#596171 change recently used to use new recently used backend
    + gnome#XXXXXX split config/data setting into xdg dirs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.4-1
- next release, drop patches

* Wed Apr 01 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.3-11
- Resolves: rhbz#226301 fix some rpmlint warnings

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Caolán McNamara <caolanm@redhat.com> - 0.14.3-9
- rebuild for e-d-s

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.14.3-8
- Rebuild for Python 2.6

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 0.14.3-7
- rebuild for e-d-s

* Thu Oct 23 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.14.3-6
- Rebuild for new camel library from e-d-s

* Mon Oct 13 2008 Caolán McNamara <caolanm@redhat.com> - 0.14.3-5
- Resolves: rhbz#466615 back-port html improvements

* Tue Sep 16 2008 Caolán McNamara <caolanm@redhat.com> - 0.14.3-4
- remove some .la files

* Tue Aug 05 2008 Caolán McNamara <caolanm@redhat.com> - 0.14.3-3
- rebuild for e-d-s

* Wed May 13 2008 Caolan McNamara <caolanm@redhat.com> - 0.14.3-2
- rebuild for e-d-s

* Thu Apr 17 2008 Caolan McNamara <caolanm@redhat.com> - 0.14.3-1
- next version

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.14.2-12
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Caolan McNamara <caolanm@redhat.com> - 0.14.2-11
- rebuild for deps

* Sat Oct 20 2007 Caolan McNamara <caolanm@redhat.com> - 0.14.2-10
- Resolves: rhbz#342891 multiarch conflicts in planner

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> - 0.14.2-9
- rebuild

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> - 0.14.2-8
- clarify license, GPLv2 + later version

* Sun Jun 10 2007 Caolan McNamara <caolanm@redhat.com> - 0.14.2-7
- Resolves: rhbz#243367 don't require yelp
  (on the bright side we picked up on evo 2.12)

* Fri Jun 08 2007 Caolan McNamara <caolanm@redhat.com> - 0.14.2-6
- Resolves: rhbz#243367 require yelp

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.14.2-5
- Move api docs to -devel

* Fri Feb 09 2007 Caolan McNamara <caolanm@redhat.com> - 0.14.2-4
- some spec cleanup

* Wed Dec 20 2006 Caolan McNamara <caolanm@redhat.com> - 0.14.2-3
- rebuild for new evolution-data-server

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.14.2-2
- rebuild for python 2.5

* Tue Nov 28 2006 Caolan McNamara <caolanm@redhat.com> - 0.14.2-1
- next version

* Fri Oct 27 2006 Matthew Barnes <mbarnes@redhat.com> - 0.14.1-3
- Update BuildRequires for evolution-devel.
- Update BuildRequires for evolution-data-server-devel.
- Update planner-0.13-enableeds.patch for Evolution 2.10.
- Update some files to _libdir/evolution/2.10.
- Rebuild against evolution-data-server-1.9.1.

* Mon Oct 16 2006 Caolan McNamara <caolanm@redhat.com> - 0.14.1-2
- Resolves: rhbz#211000
- move examples into docdir

* Mon Oct 09 2006 Caolan McNamara <caolanm@redhat.com> - 0.14.1-1
- bump to 0.14.1

* Tue Aug 08 2006 Caolan McNamara <caolanm@redhat.com> - 0.14-3
- rebuild against eds, deja-vu

* Sat Aug 05 2006 Caolan McNamara <caolanm@redhat.com> - 0.14-2
- rebuild against eds

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.14-1.1
- rebuild

* Fri Jun 23 2006 Caolan McNamara <caolanm@redhat.com> - 0.14-1
- new version

* Wed Mar 17 2006 Caolan McNamara <caolanm@redhat.com> - 0.13-5
- courtesy Stuart Clark <sclark@tpg.com.au> bug fix for: 
  Gantt bar height doesn't match treeview row height
  from bugzilla http://bugzilla.gnome.org/show_bug.cgi?id=128983
- rh#191808# Extra BuildRequires, and fix eds enabling patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.13-4.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Caolan McNamara <caolanm@redhat.com> - 0.13-4
- rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.13-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Caolan McNamara <caolanm@redhat.com> - 0.13-3
- rh#179781# add evolution data server plugin

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 30 2005 Caolan McNamara <caolanm@redhat.com> - 0.13-2
- fiddle Requires

* Thu Mar 24 2005 Dan Williams <dcbw@redhat.com> - 0.13-1
- Update to 0.13

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> - 0.12.1-4
- rebuild with gcc4

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 0.12.1-3
- rebuild against python 2.4

* Fri Oct 22 2004 Dan Williams <dcbw@redhat.com> 0.12.1-2
- #rh136296# fix libxml2-devel BuildRequires

* Thu Sep 23 2004 Jonathan Blandford <jrb@redhat.com> 0.12.1-1
- new version

* Wed Sep 22 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add ldconfig calls to post/postun

* Sun Sep 19 2004 Dan Williams <dcbw@redhat.com> 0.12-5
- Add BuildReq scrollkeeper again (#124184, #111145)
- Add Requires shared-mime-info for update-mime-database
- Fix up planner's .desktop file (#132566)

* Tue Aug 31 2004 Warren Togami <wtogami@redhat.com> 0.12-3
- #131285 proper find_lang usage

* Wed Aug 18 2004 Warren Togami <wtogami@redhat.com> 0.12-2
- BuildReq libtool, gettext, gtk-doc, libgsf-devel, pygtk2-devel

* Thu Aug  5 2004 Dan Williams <dcbw@redhat.com> 0.12-1
- Update to 0.12
- Sync specfile with Imendio specfile
- Add BuildRequires: scrollkeeper (RH #124184)
- Add obsoletes: libmrproject-devel

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 8 2004 Dan Williams <dcbw@redhat.com> 0.11-1
- Initial Release of 0.11 RPMs
