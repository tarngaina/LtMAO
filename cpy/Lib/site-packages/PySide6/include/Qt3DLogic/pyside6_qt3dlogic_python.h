// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QT3DLOGIC_PYTHON_H
#define SBK_QT3DLOGIC_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qt3dcore_python.h>
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <Qt3DLogic/qframeaction.h>

QT_BEGIN_NAMESPACE

namespace Qt3DLogic {
    class QFrameAction;
    class QLogicAspect;
}
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QT3DLOGICQT3DLOGIC_IDX                               = 0,
    SBK_QT3DLOGIC_QFRAMEACTION_IDX                           = 2,
    SBK_QT3DLOGIC_QLOGICASPECT_IDX                           = 4,
    SBK_QT3DLOGIC_IDX_COUNT                                  = 6,
};

// Type indices
enum : int {
    SBK_Qt3DLogicQt3DLogic_IDX                               = 0,
    SBK_Qt3DLogic_QFrameAction_IDX                           = 1,
    SBK_Qt3DLogic_QLogicAspect_IDX                           = 2,
    SBK_Qt3DLogic_IDX_COUNT                                  = 3,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_Qt3DLogicTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_Qt3DLogicTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_Qt3DLogicModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_Qt3DLogicTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QT3DLOGIC_QLIST_INT_IDX                              = 0, // QList<int>
    SBK_QT3DLOGIC_QLIST_QT3DCORE_QENTITYPTR_IDX              = 2, // QList<Qt3DCore::QEntity*>
    SBK_QT3DLOGIC_STD_VECTOR_QSHAREDPOINTER_QT3DCORE_QASPECTJOB_IDX = 4, // std::vector<QSharedPointer<Qt3DCore::QAspectJob>>
    SBK_QT3DLOGIC_QLIST_QVARIANT_IDX                         = 6, // QList<QVariant>
    SBK_QT3DLOGIC_QLIST_QSTRING_IDX                          = 8, // QList<QString>
    SBK_QT3DLOGIC_QMAP_QSTRING_QVARIANT_IDX                  = 10, // QMap<QString,QVariant>
    SBK_QT3DLOGIC_CONVERTERS_IDX_COUNT                       = 12,
};

// Converter indices
enum : int {
    SBK_Qt3DLogic_QList_int_IDX                              = 0, // QList<int>
    SBK_Qt3DLogic_QList_Qt3DCore_QEntityPTR_IDX              = 1, // QList<Qt3DCore::QEntity*>
    SBK_Qt3DLogic_std_vector_QSharedPointer_Qt3DCore_QAspectJob_IDX = 2, // std::vector<QSharedPointer<Qt3DCore::QAspectJob>>
    SBK_Qt3DLogic_QList_QVariant_IDX                         = 3, // QList<QVariant>
    SBK_Qt3DLogic_QList_QString_IDX                          = 4, // QList<QString>
    SBK_Qt3DLogic_QMap_QString_QVariant_IDX                  = 5, // QMap<QString,QVariant>
    SBK_Qt3DLogic_CONVERTERS_IDX_COUNT                       = 6,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::Qt3DLogic::QFrameAction >() { return Shiboken::Module::get(SbkPySide6_Qt3DLogicTypeStructs[SBK_Qt3DLogic_QFrameAction_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DLogic::QLogicAspect >() { return Shiboken::Module::get(SbkPySide6_Qt3DLogicTypeStructs[SBK_Qt3DLogic_QLogicAspect_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QT3DLOGIC_PYTHON_H

