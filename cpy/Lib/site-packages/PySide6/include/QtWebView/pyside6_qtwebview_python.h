// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTWEBVIEW_PYTHON_H
#define SBK_QTWEBVIEW_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtWebView/qtwebviewfunctions.h>

QT_BEGIN_NAMESPACE
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QTWEBVIEWQTWEBVIEW_IDX                               = 0,
    SBK_QTWEBVIEW_IDX_COUNT                                  = 2,
};

// Type indices
enum : int {
    SBK_QtWebViewQtWebView_IDX                               = 0,
    SBK_QtWebView_IDX_COUNT                                  = 1,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtWebViewTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtWebViewTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtWebViewModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtWebViewTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTWEBVIEW_QLIST_INT_IDX                              = 0, // QList<int>
    SBK_QTWEBVIEW_QLIST_QVARIANT_IDX                         = 2, // QList<QVariant>
    SBK_QTWEBVIEW_QLIST_QSTRING_IDX                          = 4, // QList<QString>
    SBK_QTWEBVIEW_QMAP_QSTRING_QVARIANT_IDX                  = 6, // QMap<QString,QVariant>
    SBK_QTWEBVIEW_CONVERTERS_IDX_COUNT                       = 8,
};

// Converter indices
enum : int {
    SBK_QtWebView_QList_int_IDX                              = 0, // QList<int>
    SBK_QtWebView_QList_QVariant_IDX                         = 1, // QList<QVariant>
    SBK_QtWebView_QList_QString_IDX                          = 2, // QList<QString>
    SBK_QtWebView_QMap_QString_QVariant_IDX                  = 3, // QMap<QString,QVariant>
    SBK_QtWebView_CONVERTERS_IDX_COUNT                       = 4,
};
// Macros for type check

#endif // SBK_QTWEBVIEW_PYTHON_H

