// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTWEBENGINEQUICK_PYTHON_H
#define SBK_QTWEBENGINEQUICK_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtqml_python.h>
#include <pyside6_qtcore_python.h>
#include <pyside6_qtnetwork_python.h>
#include <pyside6_qtwebenginecore_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtprintsupport_python.h>
#include <pyside6_qtwidgets_python.h>
#include <pyside6_qtwebchannel_python.h>

// Bound library includes
#include <QtWebEngineQuick/qquickwebengineprofile.h>
#include <QtWebEngineQuick/qtwebenginequickglobal.h>

QT_BEGIN_NAMESPACE
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QQUICKWEBENGINEPROFILE_HTTPCACHETYPE_IDX             = 2,
    SBK_QQUICKWEBENGINEPROFILE_PERSISTENTCOOKIESPOLICY_IDX   = 4,
    SBK_QQUICKWEBENGINEPROFILE_PERSISTENTPERMISSIONSPOLICY_IDX = 6,
    SBK_QQUICKWEBENGINEPROFILE_IDX                           = 0,
    SBK_QTWEBENGINEQUICKQTWEBENGINEQUICK_IDX                 = 8,
    SBK_QTWEBENGINEQUICK_IDX_COUNT                           = 10,
};

// Type indices
enum : int {
    SBK_QQuickWebEngineProfile_HttpCacheType_IDX             = 1,
    SBK_QQuickWebEngineProfile_PersistentCookiesPolicy_IDX   = 2,
    SBK_QQuickWebEngineProfile_PersistentPermissionsPolicy_IDX = 3,
    SBK_QQuickWebEngineProfile_IDX                           = 0,
    SBK_QtWebEngineQuickQtWebEngineQuick_IDX                 = 4,
    SBK_QtWebEngineQuick_IDX_COUNT                           = 5,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtWebEngineQuickTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtWebEngineQuickTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtWebEngineQuickModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtWebEngineQuickTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTWEBENGINEQUICK_QLIST_INT_IDX                       = 0, // QList<int>
    SBK_QTWEBENGINEQUICK_QLIST_QOBJECTPTR_IDX                = 2, // QList<QObject*>
    SBK_QTWEBENGINEQUICK_QLIST_QBYTEARRAY_IDX                = 4, // QList<QByteArray>
    SBK_QTWEBENGINEQUICK_QLIST_QWEBENGINEPERMISSION_IDX      = 6, // QList<QWebEnginePermission>
    SBK_QTWEBENGINEQUICK_QLIST_QVARIANT_IDX                  = 8, // QList<QVariant>
    SBK_QTWEBENGINEQUICK_QLIST_QSTRING_IDX                   = 10, // QList<QString>
    SBK_QTWEBENGINEQUICK_QMAP_QSTRING_QVARIANT_IDX           = 12, // QMap<QString,QVariant>
    SBK_QTWEBENGINEQUICK_CONVERTERS_IDX_COUNT                = 14,
};

// Converter indices
enum : int {
    SBK_QtWebEngineQuick_QList_int_IDX                       = 0, // QList<int>
    SBK_QtWebEngineQuick_QList_QObjectPTR_IDX                = 1, // QList<QObject*>
    SBK_QtWebEngineQuick_QList_QByteArray_IDX                = 2, // QList<QByteArray>
    SBK_QtWebEngineQuick_QList_QWebEnginePermission_IDX      = 3, // QList<QWebEnginePermission>
    SBK_QtWebEngineQuick_QList_QVariant_IDX                  = 4, // QList<QVariant>
    SBK_QtWebEngineQuick_QList_QString_IDX                   = 5, // QList<QString>
    SBK_QtWebEngineQuick_QMap_QString_QVariant_IDX           = 6, // QMap<QString,QVariant>
    SBK_QtWebEngineQuick_CONVERTERS_IDX_COUNT                = 7,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QQuickWebEngineProfile::HttpCacheType >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineQuickTypeStructs[SBK_QQuickWebEngineProfile_HttpCacheType_IDX]); }
template<> inline PyTypeObject *SbkType< ::QQuickWebEngineProfile::PersistentCookiesPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineQuickTypeStructs[SBK_QQuickWebEngineProfile_PersistentCookiesPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QQuickWebEngineProfile::PersistentPermissionsPolicy >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineQuickTypeStructs[SBK_QQuickWebEngineProfile_PersistentPermissionsPolicy_IDX]); }
template<> inline PyTypeObject *SbkType< ::QQuickWebEngineProfile >() { return Shiboken::Module::get(SbkPySide6_QtWebEngineQuickTypeStructs[SBK_QQuickWebEngineProfile_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTWEBENGINEQUICK_PYTHON_H

