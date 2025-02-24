// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTMULTIMEDIAWIDGETS_PYTHON_H
#define SBK_QTMULTIMEDIAWIDGETS_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtcore_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtmultimedia_python.h>
#include <pyside6_qtnetwork_python.h>
#include <pyside6_qtwidgets_python.h>

// Bound library includes

QT_BEGIN_NAMESPACE
class QGraphicsVideoItem;
class QVideoWidget;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QGRAPHICSVIDEOITEM_IDX                               = 0,
    SBK_QVIDEOWIDGET_IDX                                     = 2,
    SBK_QTMULTIMEDIAWIDGETS_IDX_COUNT                        = 4,
};

// Type indices
enum : int {
    SBK_QGraphicsVideoItem_IDX                               = 0,
    SBK_QVideoWidget_IDX                                     = 1,
    SBK_QtMultimediaWidgets_IDX_COUNT                        = 2,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtMultimediaWidgetsTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtMultimediaWidgetsTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtMultimediaWidgetsModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtMultimediaWidgetsTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTMULTIMEDIAWIDGETS_QLIST_INT_IDX                    = 0, // QList<int>
    SBK_QTMULTIMEDIAWIDGETS_QLIST_QACTIONPTR_IDX             = 2, // QList<QAction*>
    SBK_QTMULTIMEDIAWIDGETS_QLIST_QVARIANT_IDX               = 4, // QList<QVariant>
    SBK_QTMULTIMEDIAWIDGETS_QLIST_QSTRING_IDX                = 6, // QList<QString>
    SBK_QTMULTIMEDIAWIDGETS_QMAP_QSTRING_QVARIANT_IDX        = 8, // QMap<QString,QVariant>
    SBK_QTMULTIMEDIAWIDGETS_CONVERTERS_IDX_COUNT             = 10,
};

// Converter indices
enum : int {
    SBK_QtMultimediaWidgets_QList_int_IDX                    = 0, // QList<int>
    SBK_QtMultimediaWidgets_QList_QActionPTR_IDX             = 1, // QList<QAction*>
    SBK_QtMultimediaWidgets_QList_QVariant_IDX               = 2, // QList<QVariant>
    SBK_QtMultimediaWidgets_QList_QString_IDX                = 3, // QList<QString>
    SBK_QtMultimediaWidgets_QMap_QString_QVariant_IDX        = 4, // QMap<QString,QVariant>
    SBK_QtMultimediaWidgets_CONVERTERS_IDX_COUNT             = 5,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QGraphicsVideoItem >() { return Shiboken::Module::get(SbkPySide6_QtMultimediaWidgetsTypeStructs[SBK_QGraphicsVideoItem_IDX]); }
template<> inline PyTypeObject *SbkType< ::QVideoWidget >() { return Shiboken::Module::get(SbkPySide6_QtMultimediaWidgetsTypeStructs[SBK_QVideoWidget_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTMULTIMEDIAWIDGETS_PYTHON_H

