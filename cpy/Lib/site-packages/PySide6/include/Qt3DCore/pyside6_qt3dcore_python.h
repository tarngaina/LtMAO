// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only


#ifndef SBK_QT3DCORE_PYTHON_H
#define SBK_QT3DCORE_PYTHON_H

#include <sbkpython.h>
#include <sbkmodule.h>
#include <sbkconverter.h>
// Module Includes
#include <pyside6_qtgui_python.h>
#include <pyside6_qtcore_python.h>

// Bound library includes
#include <Qt3DCore/qaspectengine.h>
#include <Qt3DCore/qattribute.h>
#include <Qt3DCore/qbackendnode.h>
#include <Qt3DCore/qbuffer.h>
#include <Qt3DCore/qgeometryview.h>
#include <Qt3DCore/qnodeid.h>
#include <Qt3DCore/qskeletonloader.h>
#include <qsharedpointer.h>

QT_BEGIN_NAMESPACE

namespace Qt3DCore {
    class QAbstractAspect;
    class QAbstractFunctor;
    class QAbstractSkeleton;
    class QArmature;
    class QAspectJob;
    class QBackendNodeMapper;
    class QBoundingVolume;
    class QComponent;
    class QCoreAspect;
    class QCoreSettings;
    class QEntity;
    class QGeometry;
    class QJoint;
    class QNode;
    class QNodeId;
    struct QNodeIdTypePair;
    class QSkeleton;
    class QTransform;
}
QT_END_NAMESPACE

// Type indices
enum [[deprecated]] : int {
    SBK_QT3DCOREQT3DCORE_IDX                                 = 2,
    SBK_QT3DCORE_QABSTRACTASPECT_IDX                         = 4,
    SBK_QT3DCORE_QABSTRACTFUNCTOR_IDX                        = 6,
    SBK_QT3DCORE_QABSTRACTSKELETON_IDX                       = 8,
    SBK_QT3DCORE_QARMATURE_IDX                               = 10,
    SBK_QT3DCORE_QASPECTENGINE_RUNMODE_IDX                   = 14,
    SBK_QT3DCORE_QASPECTENGINE_IDX                           = 12,
    SBK_QT3DCORE_QASPECTJOB_IDX                              = 16,
    SBK_QT3DCORE_QATTRIBUTE_ATTRIBUTETYPE_IDX                = 20,
    SBK_QT3DCORE_QATTRIBUTE_VERTEXBASETYPE_IDX               = 22,
    SBK_QT3DCORE_QATTRIBUTE_IDX                              = 18,
    SBK_QT3DCORE_QBACKENDNODE_MODE_IDX                       = 26,
    SBK_QT3DCORE_QBACKENDNODE_IDX                            = 24,
    SBK_QT3DCORE_QBACKENDNODEMAPPER_IDX                      = 28,
    SBK_QT3DCORE_QBOUNDINGVOLUME_IDX                         = 30,
    SBK_QT3DCORE_QBUFFER_USAGETYPE_IDX                       = 36,
    SBK_QT3DCORE_QBUFFER_ACCESSTYPE_IDX                      = 34,
    SBK_QT3DCORE_QBUFFER_IDX                                 = 32,
    SBK_QT3DCORE_QCOMPONENT_IDX                              = 38,
    SBK_QT3DCORE_QCOREASPECT_IDX                             = 40,
    SBK_QT3DCORE_QCORESETTINGS_IDX                           = 42,
    SBK_QT3DCORE_QENTITY_IDX                                 = 44,
    SBK_QT3DCORE_QGEOMETRY_IDX                               = 46,
    SBK_QT3DCORE_QGEOMETRYVIEW_PRIMITIVETYPE_IDX             = 50,
    SBK_QT3DCORE_QGEOMETRYVIEW_IDX                           = 48,
    SBK_QT3DCORE_QJOINT_IDX                                  = 52,
    SBK_QT3DCORE_QNODE_IDX                                   = 54,
    SBK_QT3DCORE_QNODEID_IDX                                 = 56,
    SBK_QT3DCORE_QNODEIDTYPEPAIR_IDX                         = 58,
    SBK_QT3DCORE_QSKELETON_IDX                               = 60,
    SBK_QT3DCORE_QSKELETONLOADER_STATUS_IDX                  = 64,
    SBK_QT3DCORE_QSKELETONLOADER_IDX                         = 62,
    SBK_QT3DCORE_QTRANSFORM_IDX                              = 66,
    SBK_QSHAREDPOINTER_QT3DCORE_QENTITY_IDX                  = 68, // QSharedPointer<Qt3DCore::QEntity>
    SBK_QSHAREDPOINTER_CONSTQT3DCORE_QENTITY_IDX             = 68, // (const)
    SBK_QSHAREDPOINTER_QT3DCORE_QBACKENDNODEMAPPER_IDX       = 70, // QSharedPointer<Qt3DCore::QBackendNodeMapper>
    SBK_QSHAREDPOINTER_CONSTQT3DCORE_QBACKENDNODEMAPPER_IDX  = 70, // (const)
    SBK_QSHAREDPOINTER_QT3DCORE_QASPECTJOB_IDX               = 72, // QSharedPointer<Qt3DCore::QAspectJob>
    SBK_QSHAREDPOINTER_CONSTQT3DCORE_QASPECTJOB_IDX          = 72, // (const)
    SBK_QT3DCORE_IDX_COUNT                                   = 74,
};

// Type indices
enum : int {
    SBK_Qt3DCoreQt3DCore_IDX                                 = 1,
    SBK_Qt3DCore_QAbstractAspect_IDX                         = 2,
    SBK_Qt3DCore_QAbstractFunctor_IDX                        = 3,
    SBK_Qt3DCore_QAbstractSkeleton_IDX                       = 4,
    SBK_Qt3DCore_QArmature_IDX                               = 5,
    SBK_Qt3DCore_QAspectEngine_RunMode_IDX                   = 7,
    SBK_Qt3DCore_QAspectEngine_IDX                           = 6,
    SBK_Qt3DCore_QAspectJob_IDX                              = 8,
    SBK_Qt3DCore_QAttribute_AttributeType_IDX                = 10,
    SBK_Qt3DCore_QAttribute_VertexBaseType_IDX               = 11,
    SBK_Qt3DCore_QAttribute_IDX                              = 9,
    SBK_Qt3DCore_QBackendNode_Mode_IDX                       = 13,
    SBK_Qt3DCore_QBackendNode_IDX                            = 12,
    SBK_Qt3DCore_QBackendNodeMapper_IDX                      = 14,
    SBK_Qt3DCore_QBoundingVolume_IDX                         = 15,
    SBK_Qt3DCore_QBuffer_UsageType_IDX                       = 18,
    SBK_Qt3DCore_QBuffer_AccessType_IDX                      = 17,
    SBK_Qt3DCore_QBuffer_IDX                                 = 16,
    SBK_Qt3DCore_QComponent_IDX                              = 19,
    SBK_Qt3DCore_QCoreAspect_IDX                             = 20,
    SBK_Qt3DCore_QCoreSettings_IDX                           = 21,
    SBK_Qt3DCore_QEntity_IDX                                 = 22,
    SBK_Qt3DCore_QGeometry_IDX                               = 23,
    SBK_Qt3DCore_QGeometryView_PrimitiveType_IDX             = 25,
    SBK_Qt3DCore_QGeometryView_IDX                           = 24,
    SBK_Qt3DCore_QJoint_IDX                                  = 26,
    SBK_Qt3DCore_QNode_IDX                                   = 27,
    SBK_Qt3DCore_QNodeId_IDX                                 = 28,
    SBK_Qt3DCore_QNodeIdTypePair_IDX                         = 29,
    SBK_Qt3DCore_QSkeleton_IDX                               = 30,
    SBK_Qt3DCore_QSkeletonLoader_Status_IDX                  = 32,
    SBK_Qt3DCore_QSkeletonLoader_IDX                         = 31,
    SBK_Qt3DCore_QTransform_IDX                              = 33,
    SBK_QSharedPointer_Qt3DCore_QEntity_IDX                  = 34, // QSharedPointer<Qt3DCore::QEntity>
    SBK_QSharedPointer_constQt3DCore_QEntity_IDX             = 34, // (const)
    SBK_QSharedPointer_Qt3DCore_QBackendNodeMapper_IDX       = 35, // QSharedPointer<Qt3DCore::QBackendNodeMapper>
    SBK_QSharedPointer_constQt3DCore_QBackendNodeMapper_IDX  = 35, // (const)
    SBK_QSharedPointer_Qt3DCore_QAspectJob_IDX               = 36, // QSharedPointer<Qt3DCore::QAspectJob>
    SBK_QSharedPointer_constQt3DCore_QAspectJob_IDX          = 36, // (const)
    SBK_Qt3DCore_IDX_COUNT                                   = 37,
};

// This variable stores all Python types exported by this module.
extern Shiboken::Module::TypeInitStruct *SbkPySide6_Qt3DCoreTypeStructs;

// This variable stores all Python types exported by this module in a backwards compatible way with identical indexing.
[[deprecated]] extern PyTypeObject **SbkPySide6_Qt3DCoreTypes;

// This variable stores the Python module object exported by this module.
extern PyObject *SbkPySide6_Qt3DCoreModuleObject;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkPySide6_Qt3DCoreTypeConverters;

// Converter indices
enum [[deprecated]] : int {
    SBK_QT3DCORE_QLIST_INT_IDX                               = 0, // QList<int>
    SBK_QT3DCORE_STD_VECTOR_QSHAREDPOINTER_QT3DCORE_QASPECTJOB_IDX = 2, // std::vector<QSharedPointer<Qt3DCore::QAspectJob>>
    SBK_QT3DCORE_QLIST_QOBJECTPTR_IDX                        = 4, // QList<QObject*>
    SBK_QT3DCORE_QLIST_QBYTEARRAY_IDX                        = 6, // QList<QByteArray>
    SBK_QT3DCORE_QLIST_QT3DCORE_QNODEPTR_IDX                 = 8, // QList<Qt3DCore::QNode*>
    SBK_QT3DCORE_QLIST_QT3DCORE_QENTITYPTR_IDX               = 10, // QList<Qt3DCore::QEntity*>
    SBK_QT3DCORE_QLIST_QT3DCORE_QATTRIBUTEPTR_IDX            = 12, // QList<Qt3DCore::QAttribute*>
    SBK_QT3DCORE_QLIST_QT3DCORE_QCOMPONENTPTR_IDX            = 14, // QList<Qt3DCore::QComponent*>
    SBK_QT3DCORE_QLIST_QT3DCORE_QJOINTPTR_IDX                = 16, // QList<Qt3DCore::QJoint*>
    SBK_QT3DCORE_QLIST_QT3DCORE_QABSTRACTASPECTPTR_IDX       = 18, // QList<Qt3DCore::QAbstractAspect*>
    SBK_QT3DCORE_QLIST_QT3DCORE_QNODEID_IDX                  = 20, // QList<Qt3DCore::QNodeId>
    SBK_QT3DCORE_QLIST_QVARIANT_IDX                          = 22, // QList<QVariant>
    SBK_QT3DCORE_QLIST_QSTRING_IDX                           = 24, // QList<QString>
    SBK_QT3DCORE_QMAP_QSTRING_QVARIANT_IDX                   = 26, // QMap<QString,QVariant>
    SBK_QT3DCORE_CONVERTERS_IDX_COUNT                        = 28,
};

// Converter indices
enum : int {
    SBK_Qt3DCore_QList_int_IDX                               = 0, // QList<int>
    SBK_Qt3DCore_std_vector_QSharedPointer_Qt3DCore_QAspectJob_IDX = 1, // std::vector<QSharedPointer<Qt3DCore::QAspectJob>>
    SBK_Qt3DCore_QList_QObjectPTR_IDX                        = 2, // QList<QObject*>
    SBK_Qt3DCore_QList_QByteArray_IDX                        = 3, // QList<QByteArray>
    SBK_Qt3DCore_QList_Qt3DCore_QNodePTR_IDX                 = 4, // QList<Qt3DCore::QNode*>
    SBK_Qt3DCore_QList_Qt3DCore_QEntityPTR_IDX               = 5, // QList<Qt3DCore::QEntity*>
    SBK_Qt3DCore_QList_Qt3DCore_QAttributePTR_IDX            = 6, // QList<Qt3DCore::QAttribute*>
    SBK_Qt3DCore_QList_Qt3DCore_QComponentPTR_IDX            = 7, // QList<Qt3DCore::QComponent*>
    SBK_Qt3DCore_QList_Qt3DCore_QJointPTR_IDX                = 8, // QList<Qt3DCore::QJoint*>
    SBK_Qt3DCore_QList_Qt3DCore_QAbstractAspectPTR_IDX       = 9, // QList<Qt3DCore::QAbstractAspect*>
    SBK_Qt3DCore_QList_Qt3DCore_QNodeId_IDX                  = 10, // QList<Qt3DCore::QNodeId>
    SBK_Qt3DCore_QList_QVariant_IDX                          = 11, // QList<QVariant>
    SBK_Qt3DCore_QList_QString_IDX                           = 12, // QList<QString>
    SBK_Qt3DCore_QMap_QString_QVariant_IDX                   = 13, // QMap<QString,QVariant>
    SBK_Qt3DCore_CONVERTERS_IDX_COUNT                        = 14,
};
// Macros for type check

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace Shiboken
{

// PyType functions, to get the PyObjectType for a type T
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAbstractAspect >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAbstractAspect_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAbstractFunctor >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAbstractFunctor_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAbstractSkeleton >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAbstractSkeleton_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QArmature >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QArmature_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAspectEngine::RunMode >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAspectEngine_RunMode_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAspectEngine >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAspectEngine_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAspectJob >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAspectJob_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAttribute::AttributeType >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAttribute_AttributeType_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAttribute::VertexBaseType >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAttribute_VertexBaseType_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QAttribute >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QAttribute_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBackendNode::Mode >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBackendNode_Mode_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBackendNode >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBackendNode_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBackendNodeMapper >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBackendNodeMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBoundingVolume >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBoundingVolume_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBuffer::UsageType >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBuffer_UsageType_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBuffer::AccessType >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBuffer_AccessType_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QBuffer >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QBuffer_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QComponent >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QComponent_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QCoreAspect >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QCoreAspect_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QCoreSettings >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QCoreSettings_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QEntity >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QEntity_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QGeometry >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QGeometry_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QGeometryView::PrimitiveType >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QGeometryView_PrimitiveType_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QGeometryView >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QGeometryView_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QJoint >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QJoint_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QNode >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QNode_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QNodeId >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QNodeId_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QNodeIdTypePair >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QNodeIdTypePair_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QSkeleton >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QSkeleton_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QSkeletonLoader::Status >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QSkeletonLoader_Status_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QSkeletonLoader >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QSkeletonLoader_IDX]); }
template<> inline PyTypeObject *SbkType< ::Qt3DCore::QTransform >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_Qt3DCore_QTransform_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSharedPointer<Qt3DCore::QEntity> >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_QSharedPointer_Qt3DCore_QEntity_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSharedPointer<Qt3DCore::QBackendNodeMapper> >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_QSharedPointer_Qt3DCore_QBackendNodeMapper_IDX]); }
template<> inline PyTypeObject *SbkType< ::QSharedPointer<Qt3DCore::QAspectJob> >() { return Shiboken::Module::get(SbkPySide6_Qt3DCoreTypeStructs[SBK_QSharedPointer_Qt3DCore_QAspectJob_IDX]); }

} // namespace Shiboken

QT_WARNING_POP
#endif // SBK_QT3DCORE_PYTHON_H

