// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QTAXCONTAINER_PYTHON_H
#define SBK_QTAXCONTAINER_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtwidgets_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <QtAxContainer/qaxbase.h>
#include <QtAxContainer/qaxscript.h>
#include <QtAxContainer/qaxselect.h>

QT_BEGIN_NAMESPACE
class QAxBaseObject;
class QAxBaseWidget;
class QAxObject;
class QAxObjectInterface;
class QAxScriptManager;
class QAxWidget;
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QAXBASE_IDX                                          = 0,
    SBK_QAXBASEOBJECT_IDX                                    = 2,
    SBK_QAXBASEWIDGET_IDX                                    = 4,
    SBK_QAXOBJECT_IDX                                        = 6,
    SBK_QAXOBJECTINTERFACE_IDX                               = 8,
    SBK_QAXSCRIPT_FUNCTIONFLAGS_IDX                          = 12,
    SBK_QAXSCRIPT_IDX                                        = 10,
    SBK_QAXSCRIPTENGINE_STATE_IDX                            = 16,
    SBK_QAXSCRIPTENGINE_IDX                                  = 14,
    SBK_QAXSCRIPTMANAGER_IDX                                 = 18,
    SBK_QAXSELECT_SANDBOXINGLEVEL_IDX                        = 22,
    SBK_QAXSELECT_IDX                                        = 20,
    SBK_QAXWIDGET_IDX                                        = 24,
    SBK_QTAXCONTAINER_IDX_COUNT                              = 26,
};

// Type indices
enum : int {
    SBK_QAxBase_IDX                                          = 0,
    SBK_QAxBaseObject_IDX                                    = 1,
    SBK_QAxBaseWidget_IDX                                    = 2,
    SBK_QAxObject_IDX                                        = 3,
    SBK_QAxObjectInterface_IDX                               = 4,
    SBK_QAxScript_FunctionFlags_IDX                          = 6,
    SBK_QAxScript_IDX                                        = 5,
    SBK_QAxScriptEngine_State_IDX                            = 8,
    SBK_QAxScriptEngine_IDX                                  = 7,
    SBK_QAxScriptManager_IDX                                 = 9,
    SBK_QAxSelect_SandboxingLevel_IDX                        = 11,
    SBK_QAxSelect_IDX                                        = 10,
    SBK_QAxWidget_IDX                                        = 12,
    SBK_QtAxContainer_IDX_COUNT                              = 13,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_QtAxContainerTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_QtAxContainerTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_QtAxContainerModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_QtAxContainerTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QTAXCONTAINER_QLIST_INT_IDX                          = 0, // QList<int>
    SBK_QTAXCONTAINER_QLIST_QVARIANT_IDX                     = 2, // QList<QVariant>
    SBK_QTAXCONTAINER_QLIST_QOBJECTPTR_IDX                   = 4, // QList<QObject*>
    SBK_QTAXCONTAINER_QLIST_QBYTEARRAY_IDX                   = 6, // QList<QByteArray>
    SBK_QTAXCONTAINER_QLIST_QACTIONPTR_IDX                   = 8, // QList<QAction*>
    SBK_QTAXCONTAINER_QMAP_QSTRING_QVARIANT_IDX              = 10, // QMap<QString,QVariant>
    SBK_QTAXCONTAINER_QLIST_QSTRING_IDX                      = 12, // QList<QString>
    SBK_QTAXCONTAINER_CONVERTERS_IDX_COUNT                   = 14,
};

// Converter indices
enum : int {
    SBK_QtAxContainer_QList_int_IDX                          = 0, // QList<int>
    SBK_QtAxContainer_QList_QVariant_IDX                     = 1, // QList<QVariant>
    SBK_QtAxContainer_QList_QObjectPTR_IDX                   = 2, // QList<QObject*>
    SBK_QtAxContainer_QList_QByteArray_IDX                   = 3, // QList<QByteArray>
    SBK_QtAxContainer_QList_QActionPTR_IDX                   = 4, // QList<QAction*>
    SBK_QtAxContainer_QMap_QString_QVariant_IDX              = 5, // QMap<QString,QVariant>
    SBK_QtAxContainer_QList_QString_IDX                      = 6, // QList<QString>
    SBK_QtAxContainer_CONVERTERS_IDX_COUNT                   = 7,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::QAxBase >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxBase_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxBaseObject >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxBaseObject_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxBaseWidget >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxBaseWidget_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxObject >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxObject_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxObjectInterface >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxObjectInterface_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxScript::FunctionFlags >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxScript_FunctionFlags_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxScript >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxScript_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxScriptEngine::State >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxScriptEngine_State_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxScriptEngine >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxScriptEngine_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxScriptManager >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxScriptManager_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxSelect::SandboxingLevel >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxSelect_SandboxingLevel_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxSelect >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxSelect_IDX]); }
template<> inline PyTypeObject *SbkType< ::QAxWidget >() { return Shiboken::Module::get(SbkPySide6_QtAxContainerTypeStructs[SBK_QAxWidget_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QTAXCONTAINER_PYTHON_H

